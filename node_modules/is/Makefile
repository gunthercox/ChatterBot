
.PHONY: verify-tag release

default: release

verify-tag:
ifndef TAG
	$(error TAG is undefined)
endif

release: verify-tag
	@ OLD_TAG=`git describe --abbrev=0 --tags` && \
		npm run minify && \
		replace "$${OLD_TAG/v/}" "$(TAG)" -- *.json README.md && \
		git commit -m "v$(TAG)" *.js *.json README.md && \
		git tag "v$(TAG)"

