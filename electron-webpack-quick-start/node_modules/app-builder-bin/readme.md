# app-builder

Generic helper tool to build app in a distributable formats.
Used by [electron-builder](http://github.com/electron-userland/electron-builder) but applicable not only for building Electron applications.

```
usage: app-builder [<flags>] <command> [<args> ...]

app-builder

Flags:
  --help     Show context-sensitive help (also try --help-long and --help-man).
  --version  Show application version.

Commands:
  help [<command>...]
    Show help.


  blockmap --input=INPUT [<flags>]
    Generates file block map for differential update using content defined
    chunking (that is robust to insertions, deletions, and changes to input
    file)

    -i, --input=INPUT       input file
    -o, --output=OUTPUT     output file
    -c, --compression=gzip  compression, one of: gzip, deflate

  download --url=URL --output=OUTPUT [<flags>]
    Download file.

    -u, --url=URL        The URL.
    -o, --output=OUTPUT  The output file.
        --sha512=SHA512  The expected sha512 of file.

  download-artifact --name=NAME --url=URL [<flags>]
    Download, unpack and cache artifact from GitHub.

    -n, --name=NAME      The artifact name.
    -u, --url=URL        The artifact URL.
        --sha512=SHA512  The expected sha512 of file.

  copy --from=FROM --to=TO [<flags>]
    Copy file or dir.

    -f, --from=FROM
    -t, --to=TO
        --hard-link  Whether to use hard-links if possible

  appimage --app=APP --stage=STAGE --output=OUTPUT [<flags>]
    Build AppImage.

    -a, --app=APP                  The app dir.
    -s, --stage=STAGE              The stage dir.
    -o, --output=OUTPUT            The output file.
        --arch=x64                 The arch.
        --compression=COMPRESSION  The compression.
        --remove-stage             Whether to remove stage after build.

  snap --app=APP --stage=STAGE --output=OUTPUT [<flags>]
    Build snap.

    -t, --template=TEMPLATE  The template file.
    -u, --template-url=TEMPLATE-URL
                             The template archive URL.
        --template-sha512=TEMPLATE-SHA512
                             The expected sha512 of template archive.
    -a, --app=APP            The app dir.
    -s, --stage=STAGE        The stage dir.
        --icon=ICON          The path to the icon.
        --hooks=HOOKS        The hooks dir.
        --arch=amd64         The arch.
    -o, --output=OUTPUT      The output file.
        --docker-image="snapcore/snapcraft:latest"
                             The docker image.
        --docker             Whether to use Docker.
        --remove-stage       Whether to remove stage after build.

  icon --input=INPUT --format=FORMAT --out=OUT [<flags>]
    create ICNS or ICO or icon set from PNG files

    -i, --input=INPUT ...  input directory or file
    -f, --format=FORMAT    output format
        --out=OUT          output directory
    -r, --root=ROOT ...    base directory to resolve relative path

  dmg --volume=VOLUME [<flags>]
    Build dmg.

    --volume=VOLUME
    --icon=ICON
    --background=BACKGROUND
```