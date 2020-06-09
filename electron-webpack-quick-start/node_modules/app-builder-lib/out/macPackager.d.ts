import { Arch, AsyncTaskManager } from "builder-util";
import { SignOptions } from "electron-osx-sign";
import { Lazy } from "lazy-val";
import { AppInfo } from "./appInfo";
import { CodeSigningInfo, Identity } from "./codeSign/macCodeSign";
import { Target } from "./core";
import { AfterPackContext } from "./index";
import { MacConfiguration } from "./options/macOptions";
import { Packager } from "./packager";
import { PlatformPackager } from "./platformPackager";
export default class MacPackager extends PlatformPackager<MacConfiguration> {
    readonly codeSigningInfo: Lazy<CodeSigningInfo>;
    private _iconPath;
    constructor(info: Packager);
    readonly defaultTarget: Array<string>;
    protected prepareAppInfo(appInfo: AppInfo): AppInfo;
    getIconPath(): Promise<string | null>;
    createTargets(targets: Array<string>, mapper: (name: string, factory: (outDir: string) => Target) => void): void;
    pack(outDir: string, arch: Arch, targets: Array<Target>, taskManager: AsyncTaskManager): Promise<any>;
    private sign;
    private adjustSignOptions;
    protected doSign(opts: SignOptions): Promise<any>;
    protected doFlat(appPath: string, outFile: string, identity: Identity, keychain: string | null | undefined): Promise<any>;
    getElectronSrcDir(dist: string): string;
    getElectronDestinationDir(appOutDir: string): string;
    applyCommonInfo(appPlist: any, contentsPath: string): Promise<void>;
    protected signApp(packContext: AfterPackContext, isAsar: boolean): Promise<any>;
}
