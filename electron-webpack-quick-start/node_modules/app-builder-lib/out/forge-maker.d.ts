import { PackagerOptions } from "./packagerApi";
export interface ForgeOptions {
    readonly dir: string;
}
export declare function buildForge(forgeOptions: ForgeOptions, options: PackagerOptions): Promise<string[]>;
