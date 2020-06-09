import { Arch } from "builder-util";
import { FileTransformer } from "builder-util/out/fs";
import { Lazy } from "lazy-val";
import { CertificateFromStoreInfo, CertificateInfo, FileCodeSigningInfo } from "./codeSign/windowsCodeSign";
import { AfterPackContext } from "./configuration";
import { Target } from "./core";
import { RequestedExecutionLevel, WindowsConfiguration } from "./options/winOptions";
import { Packager } from "./packager";
import { PlatformPackager } from "./platformPackager";
import { VmManager } from "./vm/vm";
export declare class WinPackager extends PlatformPackager<WindowsConfiguration> {
    readonly cscInfo: Lazy<FileCodeSigningInfo | CertificateFromStoreInfo | null>;
    private _iconPath;
    readonly vm: Lazy<VmManager>;
    readonly computedPublisherName: Lazy<string[] | null>;
    readonly lazyCertInfo: Lazy<CertificateInfo | null>;
    readonly isForceCodeSigningVerification: boolean;
    constructor(info: Packager);
    readonly defaultTarget: Array<string>;
    protected doGetCscPassword(): string | undefined | null;
    createTargets(targets: Array<string>, mapper: (name: string, factory: (outDir: string) => Target) => void): void;
    getIconPath(): Promise<string | null>;
    sign(file: string, logMessagePrefix?: string): Promise<void>;
    private doSign;
    signAndEditResources(file: string, arch: Arch, outDir: string, internalName?: string | null, requestedExecutionLevel?: RequestedExecutionLevel | null): Promise<void>;
    private isSignDlls;
    protected createTransformerForExtraFiles(packContext: AfterPackContext): FileTransformer | null;
    protected signApp(packContext: AfterPackContext, isAsar: boolean): Promise<any>;
}
