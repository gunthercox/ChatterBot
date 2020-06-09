import { Arch } from "builder-util";
import { Target } from "./core";
import { LinuxConfiguration } from "./options/linuxOptions";
import { Packager } from "./packager";
import { PlatformPackager } from "./platformPackager";
export declare class LinuxPackager extends PlatformPackager<LinuxConfiguration> {
    readonly executableName: string;
    constructor(info: Packager);
    readonly defaultTarget: Array<string>;
    createTargets(targets: Array<string>, mapper: (name: string, factory: (outDir: string) => Target) => void): void;
}
export declare function toAppImageOrSnapArch(arch: Arch): string;
