'use strict';
const {spawn} = require('child_process');
const path = require('path');
const {format} = require('util');
const importLazy = require('import-lazy')(require);

const configstore = importLazy('configstore');
const chalk = importLazy('chalk');
const semverDiff = importLazy('semver-diff');
const latestVersion = importLazy('latest-version');
const isNpm = importLazy('is-npm');
const isInstalledGlobally = importLazy('is-installed-globally');
const isYarnGlobal = importLazy('is-yarn-global');
const hasYarn = importLazy('has-yarn');
const boxen = importLazy('boxen');
const xdgBasedir = importLazy('xdg-basedir');
const isCi = importLazy('is-ci');

const ONE_DAY = 1000 * 60 * 60 * 24;

class UpdateNotifier {
	constructor(options = {}) {
		this.options = options;
		options.pkg = options.pkg || {};
		options.distTag = options.distTag || 'latest';

		// Reduce pkg to the essential keys. with fallback to deprecated options
		// TODO: Remove deprecated options at some point far into the future
		options.pkg = {
			name: options.pkg.name || options.packageName,
			version: options.pkg.version || options.packageVersion
		};

		if (!options.pkg.name || !options.pkg.version) {
			throw new Error('pkg.name and pkg.version required');
		}

		this.packageName = options.pkg.name;
		this.packageVersion = options.pkg.version;
		this.updateCheckInterval = typeof options.updateCheckInterval === 'number' ? options.updateCheckInterval : ONE_DAY;
		this.hasCallback = typeof options.callback === 'function';
		this.callback = options.callback || (() => {});
		this.disabled = 'NO_UPDATE_NOTIFIER' in process.env ||
			process.argv.includes('--no-update-notifier') ||
			isCi();
		this.shouldNotifyInNpmScript = options.shouldNotifyInNpmScript;

		if (!this.disabled && !this.hasCallback) {
			try {
				const ConfigStore = configstore();
				this.config = new ConfigStore(`update-notifier-${this.packageName}`, {
					optOut: false,
					// Init with the current time so the first check is only
					// after the set interval, so not to bother users right away
					lastUpdateCheck: Date.now()
				});
			} catch (error) {
				// Expecting error code EACCES or EPERM
				const message =
					chalk().yellow(format(' %s update check failed ', options.pkg.name)) +
					format('\n Try running with %s or get access ', chalk().cyan('sudo')) +
					'\n to the local update config store via \n' +
					chalk().cyan(format(' sudo chown -R $USER:$(id -gn $USER) %s ', xdgBasedir().config));

				process.on('exit', () => {
					console.error('\n' + boxen()(message, {align: 'center'}));
				});
			}
		}
	}

	check() {
		if (this.hasCallback) {
			(async () => {
				try {
					this.callback(null, await this.checkNpm());
				} catch (error) {
					this.callback(error);
				}
			})();

			return;
		}

		if (
			!this.config ||
			this.config.get('optOut') ||
			this.disabled
		) {
			return;
		}

		this.update = this.config.get('update');

		if (this.update) {
			this.config.delete('update');
		}

		// Only check for updates on a set interval
		if (Date.now() - this.config.get('lastUpdateCheck') < this.updateCheckInterval) {
			return;
		}

		// Spawn a detached process, passing the options as an environment property
		spawn(process.execPath, [path.join(__dirname, 'check.js'), JSON.stringify(this.options)], {
			detached: true,
			stdio: 'ignore'
		}).unref();
	}

	async checkNpm() {
		const {distTag} = this.options;
		const latest = await latestVersion()(this.packageName, {version: distTag});

		return {
			latest,
			current: this.packageVersion,
			type: semverDiff()(this.packageVersion, latest) || distTag,
			name: this.packageName
		};
	}

	notify(options) {
		const suppressForNpm = !this.shouldNotifyInNpmScript && isNpm().isNpm;
		if (!process.stdout.isTTY || suppressForNpm || !this.update) {
			return this;
		}

		options = Object.assign({
			isGlobal: isInstalledGlobally(),
			isYarnGlobal: isYarnGlobal()()
		}, options);

		let installCommand;

		if (options.isYarnGlobal) {
			installCommand = `yarn global add ${this.packageName}`;
		} else if (hasYarn()()) {
			installCommand = `yarn add ${this.packageName}`;
		} else {
			installCommand = `npm i ${options.isGlobal ? '-g ' : ''}${this.packageName}`;
		}

		options.message = options.message || 'Update available ' + chalk().dim(this.update.current) + chalk().reset(' → ') +
			chalk().green(this.update.latest) + ' \nRun ' + chalk().cyan(installCommand) + ' to update';

		options.boxenOpts = options.boxenOpts || {
			padding: 1,
			margin: 1,
			align: 'center',
			borderColor: 'yellow',
			borderStyle: 'round'
		};

		const message = '\n' + boxen()(options.message, options.boxenOpts);

		if (options.defer === false) {
			console.error(message);
		} else {
			process.on('exit', () => {
				console.error(message);
			});

			process.on('SIGINT', () => {
				console.error('');
				process.exit();
			});
		}

		return this;
	}
}

module.exports = options => {
	const updateNotifier = new UpdateNotifier(options);
	updateNotifier.check();
	return updateNotifier;
};

module.exports.UpdateNotifier = UpdateNotifier;
