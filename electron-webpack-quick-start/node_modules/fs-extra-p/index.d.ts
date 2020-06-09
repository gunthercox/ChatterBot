import { Stats, WriteStream } from "fs"

export { WriteStream, createReadStream, createWriteStream, FSWatcher, Stats } from "fs"

export type Filter = (file: string, stat: Stats) => boolean

export interface CopyOptions {
  overwrite?: boolean
  dereference?: boolean
  filter?: RegExp | ((file: string, stat: Stats) => boolean)
  passStats?: boolean
}

export interface MoveOptions {
  overwrite?: boolean
  limit?: number
}

export function copy(src: string, dest: string, options?: CopyOptions): Promise<void>
export function copyFile(src: string, dest: string): Promise<void>

export function move(src: string, dest: string, options?: MoveOptions): Promise<void>

export function moveSync(src: string, dest: string, options?: MoveOptions): void

export function ensureFile(path: string): Promise<void>

export function ensureFileSync(path: string): void

export function createFile(file: string): Promise<void>

export function createFileSync(file: string): void

export function mkdirs(dir: string, options?: CreateDirOptions): Promise<void>

export function mkdirsSync(dir: string, options?: CreateDirOptions): void

export function mkdirp(dir: string, options?: CreateDirOptions): Promise<void>

export function mkdirpSync(dir: string, options?: CreateDirOptions): void

export function outputFile(file: string, data: any, options?: OpenOptions): Promise<void>

export function outputFileSync(file: string, data: any): void

export function outputJson(file: string, data: any, options?: JsonOptions): Promise<void>

export function outputJsonSync(file: string, data: any): void

export function readJson(file: string, options?: OpenOptions): Promise<any>

export function readJsonSync(file: string, options?: OpenOptions): any

export function remove(dir: string): Promise<void>

export function removeSync(dir: string): void

interface JsonOptions extends OpenOptions {
  spaces: number
}

export function writeJson(file: string, object: any, options?: JsonOptions): Promise<void>

export function rename(oldPath: string, newPath: string): Promise<void>

export function truncate(fd: number, len: number): Promise<void>

export function truncateSync(fd: number, len: number): void

export function chown(path: string, uid: number, gid: number): Promise<void>

export function chownSync(path: string, uid: number, gid: number): void

export function fchown(fd: number, uid: number, gid: number): Promise<void>

export function fchownSync(fd: number, uid: number, gid: number): void

export function lchown(path: string, uid: number, gid: number): Promise<void>

export function lchownSync(path: string, uid: number, gid: number): void

export function chmod(path: string, mode: string | number): Promise<void>

export function chmodSync(path: string, mode: string | number): void

export function fchmod(fd: number, mode: string | number): Promise<void>

export function fchmodSync(fd: number, mode: string | number): void

export function lchmod(path: string, mode: string | number): Promise<void>

export function lchmodSync(path: string, mode: string | number): void

export function stat(path: string): Promise<Stats>

export function statSync(path: string): Stats

export function lstat(path: string): Promise<Stats>

export function lstatSync(path: string): Stats

export function fstat(fd: number): Promise<Stats>

export function fstatSync(fd: number): Stats

export function link(srcpath: string, dstpath: string): Promise<void>

export function linkSync(srcpath: string, dstpath: string): void

export function symlink(srcpath: string, dstpath: string, type?: string): Promise<void>

export function symlinkSync(srcpath: string, dstpath: string, type?: string): void

export function readlink(path: string): Promise<string>

export function realpath(path: string): Promise<string>
export function realpath(path: string, cache: string): Promise<string>

export function realpathSync(path: string, cache?: boolean): string

export function unlink(path: string): Promise<string>

export function unlinkSync(path: string): void

export function rmdir(path: string): Promise<void>

export function rmdirSync(path: string): void

export function mkdir(path: string, mode?: string | number): Promise<void>

export function mkdirSync(path: string, mode?: string | number): void

export function mkdtemp(prefix: string): Promise<string>

export function readdir(path: string): Promise<string[]>

export function close(fd: number): Promise<void>

export function closeSync(fd: number): void

export function open(path: string, flags: string, mode?: string): Promise<number>

export function openSync(path: string, flags: string, mode?: string): number

export function utimes(path: string, atime: number, mtime: number): Promise<void>

export function utimesSync(path: string, atime: number, mtime: number): void

export function futimes(fd: number, atime: number, mtime: number): Promise<void>

export function futimesSync(fd: number, atime: number, mtime: number): void

export function fsync(fd: number): Promise<void>

export function fsyncSync(fd: number): void

export function write(fd: number, buffer: Buffer, offset?: number, length?: number, position?: number, callback?: (err: Error, written: number, buffer: Buffer) => void): Promise<number>

export function writeSync(fd: number, buffer: Buffer, offset: number, length: number, position: number): number

export function read(fd: number, buffer: Buffer, offset: number, length: number, position: number, callback?: (err: Error, bytesRead: number, buffer: Buffer) => void): Promise<number>

export function readSync(fd: number, buffer: Buffer, offset: number, length: number, position: number): number

export function readFile(filename: string, encoding: string): Promise<string>
export function readFile(filename: string, options: OpenOptions): Promise<string>
export function readFile(filename: string): Promise<Buffer>

export function readFileSync(filename: string): Buffer
export function readFileSync(filename: string, encoding: string): string
export function readFileSync(filename: string, options: OpenOptions): string

export function writeFile(filename: string, data: any, encoding?: string): Promise<void>
export function writeFile(filename: string, data: any, options?: OpenOptions): Promise<void>

export function writeFileSync(filename: string, data: any, encoding?: string): void
export function writeFileSync(filename: string, data: any, option?: OpenOptions): void

export function appendFile(filename: string, data: any, encoding?: string): Promise<void>
export function appendFile(filename: string, data: any, option?: OpenOptions): Promise<void>

export function appendFileSync(filename: string, data: any, encoding?: string): void
export function appendFileSync(filename: string, data: any, option?: OpenOptions): void

export function ensureDir(path: string, options?: CreateDirOptions): Promise<void>

export function ensureDirSync(path: string): void

export function ensureLink(path: string): Promise<void>

export function ensureLinkSync(path: string): void

export function ensureSymlink(path: string): Promise<void>

export function ensureSymlinkSync(path: string): void

export function emptyDir(path: string): Promise<void>

export function emptyDirSync(path: string): boolean

export function pathExists(path: string): Promise<boolean>

export function access(path: string | Buffer, mode?: number): Promise<void>

export function deleteFile(path: string, ignoreIfNotExists?: boolean): Promise<any>

export interface OpenOptions {
  encoding?: string
  flag?: string
  mode?: number | string
}

export interface CreateDirOptions {
  fs?: any
  mode?: number | string
}