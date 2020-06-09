/// <reference types="node" />
import { Arch, ArchType } from "builder-util";
import { Publish } from "builder-util-runtime";
export declare type TargetConfigType = Array<string | TargetConfiguration> | string | TargetConfiguration | null;
export interface TargetConfiguration {
    /**
     * The target name. e.g. `snap`.
     */
    readonly target: string;
    /**
     * The arch or list of archs.
     */
    readonly arch?: Array<ArchType> | ArchType;
}
export declare class Platform {
    name: string;
    buildConfigurationKey: string;
    nodeName: NodeJS.Platform;
    static MAC: Platform;
    static LINUX: Platform;
    static WINDOWS: Platform;
    constructor(name: string, buildConfigurationKey: string, nodeName: NodeJS.Platform);
    toString(): string;
    createTarget(type?: string | Array<string> | null, ...archs: Array<Arch>): Map<Platform, Map<Arch, Array<string>>>;
    static current(): Platform;
    static fromString(name: string): Platform;
}
export declare abstract class Target {
    readonly name: string;
    readonly isAsyncSupported: boolean;
    abstract readonly outDir: string;
    abstract readonly options: TargetSpecificOptions | null | undefined;
    protected constructor(name: string, isAsyncSupported?: boolean);
    checkOptions(): Promise<any>;
    abstract build(appOutDir: string, arch: Arch): Promise<any>;
    finishBuild(): Promise<any>;
}
export interface TargetSpecificOptions {
    /**
     The [artifact file name template](/configuration/configuration#artifact-file-name-template).
     */
    readonly artifactName?: string | null;
    publish?: Publish;
}
export declare const DEFAULT_TARGET = "default";
export declare const DIR_TARGET = "dir";
export declare type CompressionLevel = "store" | "normal" | "maximum";
export interface BeforeBuildContext {
    readonly appDir: string;
    readonly electronVersion: string;
    readonly platform: Platform;
    readonly arch: string;
}
export interface SourceRepositoryInfo {
    type?: string;
    domain?: string;
    user: string;
    project: string;
}
