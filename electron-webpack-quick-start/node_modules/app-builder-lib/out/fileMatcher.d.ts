import { PlatformSpecificBuildOptions } from "./index";
export declare const excludedNames: string;
export declare const excludedExts = "iml,hprof,orig,pyc,pyo,rbc,swp,csproj,sln,suo,xproj,cc,d.ts";
export interface GetFileMatchersOptions {
    readonly macroExpander: (pattern: string) => string;
    readonly customBuildOptions: PlatformSpecificBuildOptions;
    readonly globalOutDir: string;
    readonly defaultSrc: string;
}
