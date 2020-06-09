import { PlatformSpecificBuildOptions } from "./options/PlatformSpecificBuildOptions";
import { Packager } from "./packager";
export declare class AppInfo {
    private readonly info;
    private readonly platformSpecificOptions;
    readonly description: string;
    readonly version: string;
    readonly buildNumber: string | undefined;
    readonly buildVersion: string;
    readonly productName: string;
    readonly productFilename: string;
    constructor(info: Packager, buildVersion: string | null | undefined, platformSpecificOptions?: PlatformSpecificBuildOptions | null);
    readonly channel: string | null;
    getVersionInWeirdWindowsForm(isSetBuildNumber?: boolean): string;
    private readonly notNullDevMetadata;
    readonly companyName: string | null;
    readonly id: string;
    readonly macBundleIdentifier: string;
    readonly name: string;
    readonly linuxPackageName: string;
    readonly sanitizedName: string;
    readonly updaterCacheDirName: string;
    readonly copyright: string;
    computePackageUrl(): Promise<string | null>;
}
export declare function smarten(s: string): string;
