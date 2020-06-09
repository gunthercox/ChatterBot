import { FileTransformer } from "builder-util/out/fs";
import { Platform } from "./core";
import { LibUiFramework } from "./frameworks/LibUiFramework";
export declare class ProtonFramework extends LibUiFramework {
    readonly name = "proton";
    readonly defaultAppIdPrefix = "com.proton-native.";
    constructor(version: string, distMacOsAppName: string, isUseLaunchUi: boolean);
    getDefaultIcon(platform: Platform): string;
    createTransformer(): FileTransformer | null;
}
