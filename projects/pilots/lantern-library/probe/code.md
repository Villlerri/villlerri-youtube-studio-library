# Код главы 1: архив исходников

Сохранение в проект принимает только документы. Поэтому код пилота лежит здесь текстом, по файлу на раздел.

Восстановить файлы — из этой папки (`probe/`):

~~~~bash
python3 -I - <<'EOF'
import pathlib, re
md = pathlib.Path('code.md').read_text()
for path, body in re.findall(r'^### `([^`]+)`\n\n~~~~[^\n]*\n(.*?)\n~~~~$', md, re.S | re.M):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body + '\n')
    if p.suffix == '.sh':
        p.chmod(0o755)
    print(p)
EOF
bun install
~~~~

Затем — сборка по [README](README.md). Один файл лежит вне папки: `../script/chapter-1-dusk.estimated.srt`.

## Файлы

### `.gitignore`

~~~~
out/
node_modules/
public/ambience.wav
public/chapter1-ambience.wav
public/chapter1-voice.wav
tools/__pycache__/
~~~~

### `bun.lock`

~~~~jsonc
{
  "lockfileVersion": 2,
  "configVersion": 1,
  "workspaces": {
    "": {
      "name": "lantern-library-probe",
      "dependencies": {
        "@fontsource/cormorant-garamond": "5.2.11",
        "@fontsource/nunito-sans": "5.2.7",
        "@remotion/cli": "4.0.530",
        "react": "18.3.1",
        "react-dom": "18.3.1",
        "remotion": "4.0.530",
      },
    },
  },
  "packages": {
    "@babel/code-frame": ["@babel/code-frame@7.29.7", "", { "dependencies": { "@babel/helper-validator-identifier": "^7.29.7", "js-tokens": "^4.0.0", "picocolors": "^1.1.1" } }, "sha512-Aup7aUOfpbAUg2ROOJN6Iw5f9DMBlzu0mIkm/malLQFN/YQgO48wCj0Kxa3sEHJvPVFg7siR+qRInwXd2qhQKw=="],

    "@babel/compat-data": ["@babel/compat-data@7.29.7", "", {}, "sha512-locTkQyKvwIEgBzVrn8693ebc97F2U8ZHjbXwDXJ5Fn2TCpNwTlKcaKLkdHop5c/icOFE7qt7Q9JC5hnKNa6Gg=="],

    "@babel/core": ["@babel/core@7.29.7", "", { "dependencies": { "@babel/code-frame": "^7.29.7", "@babel/generator": "^7.29.7", "@babel/helper-compilation-targets": "^7.29.7", "@babel/helper-module-transforms": "^7.29.7", "@babel/helpers": "^7.29.7", "@babel/parser": "^7.29.7", "@babel/template": "^7.29.7", "@babel/traverse": "^7.29.7", "@babel/types": "^7.29.7", "@jridgewell/remapping": "^2.3.5", "convert-source-map": "^2.0.0", "debug": "^4.1.0", "gensync": "^1.0.0-beta.2", "json5": "^2.2.3", "semver": "^6.3.1" } }, "sha512-RgHBCvtjbOK2gXSNBNIkNoEc9qoVEtau3hj8gEqKQuL3HZAibKarWFEI3Lfm6EYKkLalOh8eSrj9b+ch9H/VBA=="],

    "@babel/generator": ["@babel/generator@7.29.8", "", { "dependencies": { "@babel/parser": "^7.29.8", "@babel/types": "^7.29.8", "@jridgewell/gen-mapping": "^0.3.12", "@jridgewell/trace-mapping": "^0.3.28", "jsesc": "^3.0.2" } }, "sha512-gZbepsdh3WDtgZKWL+vTPh71LSBrm/Y4/QDZBVCcYfmeTEEuoOYwlSy+G1StfJg+/Zy550u/3TATbm7qDbbMtg=="],

    "@babel/helper-compilation-targets": ["@babel/helper-compilation-targets@7.29.7", "", { "dependencies": { "@babel/compat-data": "^7.29.7", "@babel/helper-validator-option": "^7.29.7", "browserslist": "^4.24.0", "lru-cache": "^5.1.1", "semver": "^6.3.1" } }, "sha512-wem6WaBj4NaVYVdNhLPPVacES6ZJ+KBBfSkTMD3YZxbP3rm3Di85tJU5ljaUNhaOynt+Aj0xruhYuzQBt8n71g=="],

    "@babel/helper-globals": ["@babel/helper-globals@7.29.7", "", {}, "sha512-3nQVUAtvkKH9zahfWgw96Jc/uFOmjACE1kQz82E2lqWmHBgjzbNlsC22nuQTfahmWeQtTq5nQ/4Nnd2A1wj4zA=="],

    "@babel/helper-module-imports": ["@babel/helper-module-imports@7.29.7", "", { "dependencies": { "@babel/traverse": "^7.29.7", "@babel/types": "^7.29.7" } }, "sha512-ejHwrQQYcm9xnTivShn2IDOlIzInN34AXskvq9QicvCtEzq1Vzclu/tKF8Jq1Cg8JG2GL6/EmjgsCT7lXepE3g=="],

    "@babel/helper-module-transforms": ["@babel/helper-module-transforms@7.29.7", "", { "dependencies": { "@babel/helper-module-imports": "^7.29.7", "@babel/helper-validator-identifier": "^7.29.7", "@babel/traverse": "^7.29.7" }, "peerDependencies": { "@babel/core": "^7.0.0" } }, "sha512-UPUVSyXbOh627KiCIGQSgwWzGeBKLkaJ9PJEdrngIwMSzxLR4jS4+f1f1jb7VzBbg8nFLaYotvVPFCTqdrmTAg=="],

    "@babel/helper-string-parser": ["@babel/helper-string-parser@7.29.7", "", {}, "sha512-Pb5ijPrZ89GDH8223L4UP8i6QApWxs04RbPQJTeWDV0/keR2E36MeKnyr6LYmUUvqRRI+Iv87SuF1W6ErINzYw=="],

    "@babel/helper-validator-identifier": ["@babel/helper-validator-identifier@7.29.7", "", {}, "sha512-qehxGkRj55h/ff8EMaJ+cYhyaKlHIxqYDn682wQD7RNp9UujOQsHog2uS0r2vzr4pW+sXf90NeeayjcNaX3fFg=="],

    "@babel/helper-validator-option": ["@babel/helper-validator-option@7.29.7", "", {}, "sha512-N9ZErrD+yW5geCDtBqnOoxmR8+tNKiGuxKlDpuJxfsqpa2dFcexaziGAE/qoHLiDDreVNMupxGmSoNlyvsA3gw=="],

    "@babel/helpers": ["@babel/helpers@7.29.10", "", { "dependencies": { "@babel/template": "^7.29.7", "@babel/types": "^7.29.8" } }, "sha512-EMCx3AGZ3WfAl6ht7AyQoPm2Lh+BGYEMdc4Q6Hf7uSCDOZFuLq44qNwL+iaim8VlyYhRAo4X43+weadK8ZB4Yg=="],

    "@babel/parser": ["@babel/parser@7.24.1", "", { "bin": "./bin/babel-parser.js" }, "sha512-Zo9c7N3xdOIQrNip7Lc9wvRPzlRtovHVE4lkz8WEDr7uYh/GMQhSiIgFxGIArRHYdJE5kxtZjAf8rT0xhdLCzg=="],

    "@babel/template": ["@babel/template@7.29.7", "", { "dependencies": { "@babel/code-frame": "^7.29.7", "@babel/parser": "^7.29.7", "@babel/types": "^7.29.7" } }, "sha512-puq+Gf35oI24FeN11LkoUQFqv9uwNeWpxXZi/Ji3rRIoKAzKnxRaZ+Gkj0vKS9ZCiTESfng1N9LyOyXvo+m+Gg=="],

    "@babel/traverse": ["@babel/traverse@7.29.10", "", { "dependencies": { "@babel/code-frame": "^7.29.7", "@babel/generator": "^7.29.8", "@babel/helper-globals": "^7.29.7", "@babel/parser": "^7.29.9", "@babel/template": "^7.29.7", "@babel/types": "^7.29.8", "debug": "^4.3.1" } }, "sha512-B3lYAs2nkKskbgQ1nfy8Ma9ao9Q1rntTAQHrzzyDuj+TSO+X3le6PfWwqDvodsb+OumE10eMFfuMCTQSQ5iuIQ=="],

    "@babel/types": ["@babel/types@7.24.0", "", { "dependencies": { "@babel/helper-string-parser": "^7.23.4", "@babel/helper-validator-identifier": "^7.22.20", "to-fast-properties": "^2.0.0" } }, "sha512-+j7a5c253RfKh8iABBhywc8NSfP5LURe7Uh4qpsh6jc+aLJguvmIUBdjSdEMQv2bENrCR5MfRdjGo7vzS/ob7w=="],

    "@emnapi/core": ["@emnapi/core@1.11.3", "", { "dependencies": { "@emnapi/wasi-threads": "1.2.3", "tslib": "^2.4.0" } }, "sha512-zLpS5asjEb7lq8jYLq37N6XKaE41DIexlY1rF/z4/tIl3wo13Sqm28fRyfIsKZD+NZ8mM5RoKkpW/rBcuoSZSg=="],

    "@emnapi/runtime": ["@emnapi/runtime@1.11.3", "", { "dependencies": { "tslib": "^2.4.0" } }, "sha512-Xz4Tpyki7XyrpbUK1jR1AhdAdaXyhhY4lZ3neLodmhpuWfy2PAQN5B46sAiU4liOXGLkHypn/qU+jvfWSCYYLA=="],

    "@emnapi/wasi-threads": ["@emnapi/wasi-threads@1.2.3", "", { "dependencies": { "tslib": "^2.4.0" } }, "sha512-ELEBe8PsLvvJ6QMr0zLt8ffvOHW/dc1m3CEzNMg7aJUv3bMaoDtw2TXyDAwkYBuroxxuHEwhRTLJSe5sya547g=="],

    "@esbuild/aix-ppc64": ["@esbuild/aix-ppc64@0.28.1", "", { "os": "aix", "cpu": "ppc64" }, "sha512-Svl7tq8k/08+p6CXPpRjQ1fKX+1odH/BQbb48fV6fj3CWHhsoIOoY87w1oHXm0qEpkIK3ZfVgp0hed3XBXzXMQ=="],

    "@esbuild/android-arm": ["@esbuild/android-arm@0.28.1", "", { "os": "android", "cpu": "arm" }, "sha512-0k2F129Xdio1TdJfzJ8sy1Q47vUD2NnwdhiAf7drUN1EBTfPf4hsFCtmMgu/6m8JSzsBrlmVjudMBQqOfG8usQ=="],

    "@esbuild/android-arm64": ["@esbuild/android-arm64@0.28.1", "", { "os": "android", "cpu": "arm64" }, "sha512-34EGEbCIAgosYz6goLcopX6Mo7NyGv9tfwEM2/7Ce2VcVRk568iSvniGWcUXIy7wEDR1wzolcxcriFVrWYcwBg=="],

    "@esbuild/android-x64": ["@esbuild/android-x64@0.28.1", "", { "os": "android", "cpu": "x64" }, "sha512-dbwY7ltSMDWsRatcRpCnES4F+im88OCUgGZjy52shC7GqHRE/cYlxNbB4Z4UpJswpcc4Qxd2oE/ufM0p61IKng=="],

    "@esbuild/darwin-arm64": ["@esbuild/darwin-arm64@0.28.1", "", { "os": "darwin", "cpu": "arm64" }, "sha512-TZbWkQY7kvTAXbXUT7uVACR5cMHsDiSz9z7ZKAX/RTq/WJEk3QyRr0wZpNhBDX+/0CtdqUIJlOiodQcta6tY3Q=="],

    "@esbuild/darwin-x64": ["@esbuild/darwin-x64@0.28.1", "", { "os": "darwin", "cpu": "x64" }, "sha512-zfdzgK9ACBNZLI/CyHTOx81SyNbM6YXn7rxSgX97VjyiPl9W1i4Ka4fgKECEoFCKGpvBj5qArWIGgQjOwkgskQ=="],

    "@esbuild/freebsd-arm64": ["@esbuild/freebsd-arm64@0.28.1", "", { "os": "freebsd", "cpu": "arm64" }, "sha512-wG2EA8ENdEI0qhkSZMjfqrdY+ziCYCPMmtZjjIwOmXFjmyzEHn+UUxk5of+SYsjtfs3VpnlC7QLzSI5hY/rOAw=="],

    "@esbuild/freebsd-x64": ["@esbuild/freebsd-x64@0.28.1", "", { "os": "freebsd", "cpu": "x64" }, "sha512-i7dZ9vQgnvSCzi/rYCXNgtF/U+eKZNJBzu3eTQbRgHnM7tNSizLOkRFAl3qzVc/Op/u5YkHHa4pf/3DOYHthLQ=="],

    "@esbuild/linux-arm": ["@esbuild/linux-arm@0.28.1", "", { "os": "linux", "cpu": "arm" }, "sha512-qVXBOHQS+d5Y722GwJzJUtOLlX7km3CraOaGormF1pDtPd2C/l1SHRPgjLunLGe51Sh5YYWKMFDyV4SxgMQYTQ=="],

    "@esbuild/linux-arm64": ["@esbuild/linux-arm64@0.28.1", "", { "os": "linux", "cpu": "arm64" }, "sha512-yHs+0uc8+nvEAfAfxrWQKK5peSNzBc4PegcMO0EJ2hT71uA7vB8Ihg2e77R2P7SG5uYjPbHlLLmve4LLLRCf0g=="],

    "@esbuild/linux-ia32": ["@esbuild/linux-ia32@0.28.1", "", { "os": "linux", "cpu": "ia32" }, "sha512-d1z4ZuP0ajrfz/FhGT4vv278rX8KnPPJx8i5+AtK7TYbx9Le9F1hyzurZpkEyjkGa9dUGhQow4C1NmeGvqxN2w=="],

    "@esbuild/linux-loong64": ["@esbuild/linux-loong64@0.28.1", "", { "os": "linux", "cpu": "none" }, "sha512-M5sRjUVZrkm1OAPR3dlOYzNmN+loZKGVi1VUQGrwuqLcbR6qeAz+famMhjASeH3YVKvZz+zT1jlh/keC3Rj/lg=="],

    "@esbuild/linux-mips64el": ["@esbuild/linux-mips64el@0.28.1", "", { "os": "linux", "cpu": "none" }, "sha512-mRObBZeHh2OxcBFPWE/FjylkRgZdYuiTR3vaTozquCGOH14iP9oN4x4Ge81CoIDYQrXmIxpFumJBu5MtZpnQJQ=="],

    "@esbuild/linux-ppc64": ["@esbuild/linux-ppc64@0.28.1", "", { "os": "linux", "cpu": "ppc64" }, "sha512-slScBsMAb3GFDcdrCgLwZtPYRoH2H/youv10QiZyRjmsP48fznoveWytSgCI/R0ZcUgpc0ZhIUEx6LHts8yrfQ=="],

    "@esbuild/linux-riscv64": ["@esbuild/linux-riscv64@0.28.1", "", { "os": "linux", "cpu": "none" }, "sha512-kw0owk1o0GFETUJyW0jc0G4Yzs0BHZn0JDZ8JRT088vjJYX777BAs1fDGxAC+q831qOs2DTC96mNsG2opdfyyQ=="],

    "@esbuild/linux-s390x": ["@esbuild/linux-s390x@0.28.1", "", { "os": "linux", "cpu": "s390x" }, "sha512-/lAIjX8aYFRByhh6L5rYtPEDRqa9de/4V/juOXcta5frjvzXO4/sqEtyytse0g3zZFuWu5cDN0MkLz2qRDD2Ag=="],

    "@esbuild/linux-x64": ["@esbuild/linux-x64@0.28.1", "", { "os": "linux", "cpu": "x64" }, "sha512-u/anNYF2mmVOEDwLtnQ1wOr3EZ9sTNGLWrsYGYwHWzGA3Si84IOkHXlbWTD1NB+9/1lcnweYKO54uhxZydNzfA=="],

    "@esbuild/netbsd-arm64": ["@esbuild/netbsd-arm64@0.28.1", "", { "os": "none", "cpu": "arm64" }, "sha512-oks0DYbLwWMmaakTsCb+zL4E+aHRVLom9IJZOAthMQEPiQmydXHkziYEsGYRx0uNV/IjEKGAV941JzH02pflqw=="],

    "@esbuild/netbsd-x64": ["@esbuild/netbsd-x64@0.28.1", "", { "os": "none", "cpu": "x64" }, "sha512-aeL6lAnN89Hz43Mlh1G8ARasbuoYvSITDEx0tHh5b7jJnHcssqgjy9Yx430GDpmCa6OyrKoS0aNRjKundRizGg=="],

    "@esbuild/openbsd-arm64": ["@esbuild/openbsd-arm64@0.28.1", "", { "os": "openbsd", "cpu": "arm64" }, "sha512-MEFJe5C3R8pwXdZ5Y21oo6m7ePiS0d9pWucn99O/wvyJZChoIQKrQDxKrGeW8F5+T0okTHesAmDeiHDTIq0V/Q=="],

    "@esbuild/openbsd-x64": ["@esbuild/openbsd-x64@0.28.1", "", { "os": "openbsd", "cpu": "x64" }, "sha512-i/ZLIOafE0Z8cI/XANJAixoJL/uRAoS2xOA3rb0xN+KK0K177cMAsQYkzHtBrtMXAKuAc7HGgcWiZ/sRC1Nxgw=="],

    "@esbuild/openharmony-arm64": ["@esbuild/openharmony-arm64@0.28.1", "", { "os": "none", "cpu": "arm64" }, "sha512-ge+Z7EXFNt2BO1oAMsVpiQ8EwndV9i1xXerAeTIK7AtPs3bKFXQM7nlRxDSIUIMeueR1CNXxqztLzdNeReKBJg=="],

    "@esbuild/sunos-x64": ["@esbuild/sunos-x64@0.28.1", "", { "os": "sunos", "cpu": "x64" }, "sha512-BEjgtECkL3vY+SaSQ6nzVfiALUeFxpawyp8Jmf5PtYhf1Ug40N1h/hxlhts+f1FvSvarEigdxS3BlSMI2PJLcQ=="],

    "@esbuild/win32-arm64": ["@esbuild/win32-arm64@0.28.1", "", { "os": "win32", "cpu": "arm64" }, "sha512-lCv9eK/H6ZJWbE7bh2nw54CZ9M2nupBxJcTsdk/QQnWkdSjKGuxmmH8/GWrlT1eMmZfn4dGcCjRte397WqfQXA=="],

    "@esbuild/win32-ia32": ["@esbuild/win32-ia32@0.28.1", "", { "os": "win32", "cpu": "ia32" }, "sha512-zvb/mB2bSCoJOpoCBgYKKpX6YM6mJBlBUVUtVj41DlZJVEB6/0CKlRYxP5wWl1C1ILiCoAU5wZZ4q1P3qeS6Eg=="],

    "@esbuild/win32-x64": ["@esbuild/win32-x64@0.28.1", "", { "os": "win32", "cpu": "x64" }, "sha512-bm4Mowrv+GXMlpWX++EcXw/iLyd1o3+bJkC2DkWXYVvgZCqD/bSj9ctZeAMC3cIxgjRVR2Dufaiu4YPxr5gW1A=="],

    "@fontsource/cormorant-garamond": ["@fontsource/cormorant-garamond@5.2.11", "", {}, "sha512-5JjpN023lhA5soijgVT0BdRGzmlijm402ppjccMd6h+vRE0mX2lJnE+41UPfnlidrkV9/rCo1mf58WZlHnB0CA=="],

    "@fontsource/nunito-sans": ["@fontsource/nunito-sans@5.2.7", "", {}, "sha512-Vh+xhMsrH1eA9Q83Va82su3rDmNilYg+ur/TfHAOyr5kTpCOWMB8B1tDoJvSe+yJPpZ2jEWtnBHGqI2LUPVxUA=="],

    "@jridgewell/gen-mapping": ["@jridgewell/gen-mapping@0.3.13", "", { "dependencies": { "@jridgewell/sourcemap-codec": "^1.5.0", "@jridgewell/trace-mapping": "^0.3.24" } }, "sha512-2kkt/7niJ6MgEPxF0bYdQ6etZaA+fQvDcLKckhy1yIQOzaoKjBBjSj63/aLVjYE3qhRt5dvM+uUyfCg6UKCBbA=="],

    "@jridgewell/remapping": ["@jridgewell/remapping@2.3.5", "", { "dependencies": { "@jridgewell/gen-mapping": "^0.3.5", "@jridgewell/trace-mapping": "^0.3.24" } }, "sha512-LI9u/+laYG4Ds1TDKSJW2YPrIlcVYOwi2fUC6xB43lueCjgxV4lffOCZCtYFiH6TNOX+tQKXx97T4IKHbhyHEQ=="],

    "@jridgewell/resolve-uri": ["@jridgewell/resolve-uri@3.1.2", "", {}, "sha512-bRISgCIjP20/tbWSPWMEi54QVPRZExkuD9lJL+UIxUKtwVJA8wW1Trb1jMs1RFXo1CBTNZ/5hpC9QvmKWdopKw=="],

    "@jridgewell/source-map": ["@jridgewell/source-map@0.3.11", "", { "dependencies": { "@jridgewell/gen-mapping": "^0.3.5", "@jridgewell/trace-mapping": "^0.3.25" } }, "sha512-ZMp1V8ZFcPG5dIWnQLr3NSI1MiCU7UETdS/A0G8V/XWHvJv3ZsFqutJn1Y5RPmAPX6F3BiE397OqveU/9NCuIA=="],

    "@jridgewell/sourcemap-codec": ["@jridgewell/sourcemap-codec@1.6.0", "", {}, "sha512-T7jf+5zgsZHwNJ4lvQ7/aezbyk0nNX+zJVWpmHA7VYsEx7a7qr5Rg5IbtJFqkgze5Y2sruq1RUY8Q837Od7iFw=="],

    "@jridgewell/trace-mapping": ["@jridgewell/trace-mapping@0.3.31", "", { "dependencies": { "@jridgewell/resolve-uri": "^3.1.0", "@jridgewell/sourcemap-codec": "^1.4.14" } }, "sha512-zzNR+SdQSDJzc8joaeP8QQoCQr8NuYx2dIIytl1QeBEZHJ9uW6hebsrYgbz8hJwUQao3TWCMtmfV8Nu1twOLAw=="],

    "@mediabunny/aac-encoder": ["@mediabunny/aac-encoder@1.56.1", "", { "peerDependencies": { "mediabunny": "^1.0.0" } }, "sha512-a+OY/BctP7zC4G/prHikooOVaoWXMD4+bUyEwHg2dtQiQdIwC6TDJdVYJu5dfrdSNOiAFkv1HKcYEeROdwMezg=="],

    "@mediabunny/flac-encoder": ["@mediabunny/flac-encoder@1.56.1", "", { "peerDependencies": { "mediabunny": "^1.0.0" } }, "sha512-zbmorMVlF1izwtlz5mWnu7A1rJLM+V26I0pEFr9Td1EDTwE5uAGRSW+/UZlnjwj1t00Woe3Zonfh9kb7lRRBqg=="],

    "@mediabunny/mp3-encoder": ["@mediabunny/mp3-encoder@1.56.1", "", { "peerDependencies": { "mediabunny": "^1.0.0" } }, "sha512-p66ovEq6mZt3ejje45NOju84hIJI4v8rHfsmc1D2J34ziV0USE8AdJBzmiwqxl6nZkIAQLNB19HzbVRcQfc51g=="],

    "@module-federation/error-codes": ["@module-federation/error-codes@0.22.0", "", {}, "sha512-xF9SjnEy7vTdx+xekjPCV5cIHOGCkdn3pIxo9vU7gEZMIw0SvAEdsy6Uh17xaCpm8V0FWvR0SZoK9Ik6jGOaug=="],

    "@module-federation/runtime": ["@module-federation/runtime@0.22.0", "", { "dependencies": { "@module-federation/error-codes": "0.22.0", "@module-federation/runtime-core": "0.22.0", "@module-federation/sdk": "0.22.0" } }, "sha512-38g5iPju2tPC3KHMPxRKmy4k4onNp6ypFPS1eKGsNLUkXgHsPMBFqAjDw96iEcjri91BrahG4XcdyKi97xZzlA=="],

    "@module-federation/runtime-core": ["@module-federation/runtime-core@0.22.0", "", { "dependencies": { "@module-federation/error-codes": "0.22.0", "@module-federation/sdk": "0.22.0" } }, "sha512-GR1TcD6/s7zqItfhC87zAp30PqzvceoeDGYTgF3Vx2TXvsfDrhP6Qw9T4vudDQL3uJRne6t7CzdT29YyVxlgIA=="],

    "@module-federation/runtime-tools": ["@module-federation/runtime-tools@0.22.0", "", { "dependencies": { "@module-federation/runtime": "0.22.0", "@module-federation/webpack-bundler-runtime": "0.22.0" } }, "sha512-4ScUJ/aUfEernb+4PbLdhM/c60VHl698Gn1gY21m9vyC1Ucn69fPCA1y2EwcCB7IItseRMoNhdcWQnzt/OPCNA=="],

    "@module-federation/sdk": ["@module-federation/sdk@0.22.0", "", {}, "sha512-x4aFNBKn2KVQRuNVC5A7SnrSCSqyfIWmm1DvubjbO9iKFe7ith5niw8dqSFBekYBg2Fwy+eMg4sEFNVvCAdo6g=="],

    "@module-federation/webpack-bundler-runtime": ["@module-federation/webpack-bundler-runtime@0.22.0", "", { "dependencies": { "@module-federation/runtime": "0.22.0", "@module-federation/sdk": "0.22.0" } }, "sha512-aM8gCqXu+/4wBmJtVeMeeMN5guw3chf+2i6HajKtQv7SJfxV/f4IyNQJUeUQu9HfiAZHjqtMV5Lvq/Lvh8LdyA=="],

    "@napi-rs/wasm-runtime": ["@napi-rs/wasm-runtime@1.0.7", "", { "dependencies": { "@emnapi/core": "^1.5.0", "@emnapi/runtime": "^1.5.0", "@tybys/wasm-util": "^0.10.1" } }, "sha512-SeDnOO0Tk7Okiq6DbXmmBODgOAb9dp9gjlphokTUxmt8U3liIP1ZsozBahH69j/RJv+Rfs6IwUKHTgQYJ/HBAw=="],

    "@remotion/bundler": ["@remotion/bundler@4.0.530", "", { "dependencies": { "@remotion/media-parser": "4.0.530", "@remotion/studio": "4.0.530", "@remotion/studio-shared": "4.0.530", "@remotion/timeline-utils": "4.0.530", "@rspack/core": "1.7.11", "@rspack/plugin-react-refresh": "1.6.1", "css-loader": "7.1.4", "esbuild": "0.28.1", "react-refresh": "0.18.0", "remotion": "4.0.530", "style-loader": "4.0.0", "webpack": "5.105.0" }, "peerDependencies": { "react": ">=16.8.0", "react-dom": ">=16.8.0" } }, "sha512-kIKGcfV53nSi0KdrVwFmuNtsUEKShzR1EQ0UH/hVUxIh4z3tmxa7nMC7XX1rj0fJ4id0UT2wCqas6kD5DvpDlg=="],

    "@remotion/canvas": ["@remotion/canvas@4.0.530", "", { "dependencies": { "@remotion/player": "4.0.530", "@remotion/studio-shared": "4.0.530", "remotion": "4.0.530" }, "peerDependencies": { "react": ">=16.8.0", "react-dom": ">=16.8.0" } }, "sha512-kKvrVKFqzvK4Mq5EYfRu+yZsBkor8I41crPJu9wavMCtkAFf5XIZZNJTZ13CI/Iq8NKASANqBoRFUM91N4Undg=="],

    "@remotion/captions": ["@remotion/captions@4.0.530", "", {}, "sha512-KpIG/jA5fJ/hTh2185MJ+yaodSNeHgQiMYwkVSOiaIJp82WJfzpqypGrU2PSYC4ty/K6ov0pj0lJQAcmoVRZeg=="],

    "@remotion/cli": ["@remotion/cli@4.0.530", "", { "dependencies": { "@babel/parser": "7.24.1", "@remotion/bundler": "4.0.530", "@remotion/media-utils": "4.0.530", "@remotion/player": "4.0.530", "@remotion/renderer": "4.0.530", "@remotion/studio": "4.0.530", "@remotion/studio-server": "4.0.530", "@remotion/studio-shared": "4.0.530", "dotenv": "17.3.1", "minimist": "1.2.6", "prompts": "2.4.2", "remotion": "4.0.530", "semver": "7.5.3" }, "peerDependencies": { "react": ">=16.8.0", "react-dom": ">=16.8.0" }, "bin": { "remotion": "remotion-cli.js", "remotionb": "remotionb-cli.js", "remotiond": "remotiond-cli.js" } }, "sha512-Ur3Lq1EqbEE3/ecYusb+vPPdWUAOWKLbMW3PiDNxa1aAOMuleQuoZzmRENUmr4qKguDRyV5HZNf1HTfs0c+ePQ=="],

    "@remotion/codemods": ["@remotion/codemods@4.0.530", "", { "dependencies": { "@babel/parser": "7.24.1", "@babel/types": "7.24.0", "@remotion/studio-protocol": "4.0.530", "@remotion/studio-shared": "4.0.530", "ast-types": "0.16.1", "recast": "0.23.21", "remotion": "4.0.530" } }, "sha512-mvJQ6MLgr9brWKTlKbrr7w9NPl0Hpsbm7r+HEk1DF/gLtKP7bgVt7H/ztOApDG3T8UrcCC1o2nH4tiqAWwY+CA=="],

    "@remotion/compositor-darwin-arm64": ["@remotion/compositor-darwin-arm64@4.0.530", "", { "os": "darwin", "cpu": "arm64" }, "sha512-Dh4mm8Buw3Dm0/gfHTqc6ZM/+2BBupoWtodTGbDpRNB9lXrawKFNnfNzXk/pqXrb2rUd1uDgAiFUmpt10Xa3zQ=="],

    "@remotion/compositor-darwin-x64": ["@remotion/compositor-darwin-x64@4.0.530", "", { "os": "darwin", "cpu": "x64" }, "sha512-pEYto9+JfMAuzqjFTDNbzwEBtLOg4vanO/68kFYEebnP/Y4qBSLAOZihudPVQdoxqlUBK+OrvauaZceOR1JTEg=="],

    "@remotion/compositor-linux-arm64-gnu": ["@remotion/compositor-linux-arm64-gnu@4.0.530", "", { "os": "linux", "cpu": "arm64" }, "sha512-2sHLT4e0BP9vSFWPhylX4tWHL3VC3eAl90SdcgN6ZA3dU/XcMDYwW+ceYhdeM7Ryh5dOXkqhLLN/HoyJrfwegA=="],

    "@remotion/compositor-linux-arm64-musl": ["@remotion/compositor-linux-arm64-musl@4.0.530", "", { "os": "linux", "cpu": "arm64" }, "sha512-eqYokUW0SyqK6YnjJivh6v6JFqpvgCnqniVZULM8o7f/wBB8sxDOtNuk8Jy0VISPgBFtVVKDdt9smFTNbeO3dQ=="],

    "@remotion/compositor-linux-x64-gnu": ["@remotion/compositor-linux-x64-gnu@4.0.530", "", { "os": "linux", "cpu": "x64" }, "sha512-Gn6d7zenyWrkZumMLBwUWg73wVcRe554EYEFdz/SvpglqCgLlOSpA/lBrCp9hU05QXCPyOpMzWXo6BCrLx7wqg=="],

    "@remotion/compositor-linux-x64-musl": ["@remotion/compositor-linux-x64-musl@4.0.530", "", { "os": "linux", "cpu": "x64" }, "sha512-8/l0t9P0zX2rd8Ootp7iUJy0u08Ce5KexG8YJI7VRYseqcKkuZnvOFts4SKKC+nGKEf9CeWYVQjsN7dj/rXnJA=="],

    "@remotion/compositor-win32-x64-msvc": ["@remotion/compositor-win32-x64-msvc@4.0.530", "", { "os": "win32", "cpu": "x64" }, "sha512-XP/jYCNa/4ITubAUdM2NVzXL+pCyjpglR6Hdm850n0LgophKcMRjyA4CUC0kHqKV5wCtLL9aX3ZD5KuvPHnkcw=="],

    "@remotion/elevenlabs": ["@remotion/elevenlabs@4.0.530", "", { "dependencies": { "@remotion/captions": "4.0.530", "zod": "4.5.4" } }, "sha512-NbYbB9El/FfCaXRK0WueeLep/mYGL+rw+26JyW5oVyRBFt/M5nxOpIUL/kz+0oCUyKiFMBoRA4skBpvgiE2HWw=="],

    "@remotion/licensing": ["@remotion/licensing@4.0.530", "", {}, "sha512-xMnT4tT/cEcjF7CdcOP3V1pE4uMp7y6T2+vv74DQnFE0XcyU8QlwwjD/28uubprk/rLEw8F5cUHwzWDYuec90g=="],

    "@remotion/media": ["@remotion/media@4.0.530", "", { "dependencies": { "mediabunny": "1.56.1", "remotion": "4.0.530", "zod": "4.5.4" }, "peerDependencies": { "react": ">=16.8.0", "react-dom": ">=16.8.0" } }, "sha512-oI8/4WivgRT1ywnPalpihq3wD95yYF2ZBXJ1A7cnPRDiyuynYzeHe4f87OWDLYsQbsvp7m5LdlaTMetZc2VMUg=="],

    "@remotion/media-parser": ["@remotion/media-parser@4.0.530", "", {}, "sha512-0kjn93BmeANiTQ7KNP8f06zU74pyrodCRUg3o21mabfQnIZ6SwFYdYyCl7drWIz9G6PDjEGvsQXAgdwa1VwvtA=="],

    "@remotion/media-utils": ["@remotion/media-utils@4.0.530", "", { "dependencies": { "mediabunny": "1.56.1", "remotion": "4.0.530" }, "peerDependencies": { "react": ">=16.8.0", "react-dom": ">=16.8.0" } }, "sha512-ZP+wK2sdumVW3vkjeGzrVGVBIdRllqKgCmDPbqF2dP+xkJP8yzIfnhVbzn6f50wSDo2Z0hXJg2De0CAx+zreBA=="],

    "@remotion/openai-whisper": ["@remotion/openai-whisper@4.0.530", "", { "dependencies": { "@remotion/captions": "4.0.530", "zod": "4.5.4" } }, "sha512-POCg/a3yxfvYK6SoQXy0h1Xv3BFtH0yQYE8j7rrcnOKK+IH4YxQ1Gbuqs076wRx/enLHuZQKWp5b2npa5exNJg=="],

    "@remotion/paths": ["@remotion/paths@4.0.530", "", { "dependencies": { "remotion": "4.0.530" } }, "sha512-8p5PIb6xje/JwU4g5d18HG01GFlAWFAqS0NwDiz6yE+d46uTUPGmVlaeTjYfwaATYIod+SdicnaU4Oh6Tlhy9g=="],

    "@remotion/player": ["@remotion/player@4.0.530", "", { "dependencies": { "remotion": "4.0.530" }, "peerDependencies": { "react": ">=16.8.0", "react-dom": ">=16.8.0" } }, "sha512-eqKGEOB29wOZp8E8L8zIRTPmfYH4BmQwKIyMYRt3NK0vC1uShGDm9c2gTV/aiO2098GYfdP/BtRxWMtcazym8A=="],

    "@remotion/renderer": ["@remotion/renderer@4.0.530", "", { "dependencies": { "@remotion/licensing": "4.0.530", "@remotion/streaming": "4.0.530", "execa": "5.1.1", "remotion": "4.0.530", "source-map": "0.8.0", "ws": "8.21.0" }, "optionalDependencies": { "@remotion/compositor-darwin-arm64": "4.0.530", "@remotion/compositor-darwin-x64": "4.0.530", "@remotion/compositor-linux-arm64-gnu": "4.0.530", "@remotion/compositor-linux-arm64-musl": "4.0.530", "@remotion/compositor-linux-x64-gnu": "4.0.530", "@remotion/compositor-linux-x64-musl": "4.0.530", "@remotion/compositor-win32-x64-msvc": "4.0.530" }, "peerDependencies": { "react": ">=16.8.0", "react-dom": ">=16.8.0" } }, "sha512-B7kjM+SpIdPE7WrJviEHjSRJFfCg3zIJg/Gm9uHNtfhDw2d6QKyuJxhmef2vjVm9mPK54nkvV6sOq/cjmL8G/g=="],

    "@remotion/streaming": ["@remotion/streaming@4.0.530", "", {}, "sha512-V6GfSZvHXkoOsgDHsZXr/WeVXR/IQ8n7EUnZCk5ApZu4u0pzwPM/gfWWrH+SDcAKe4MLYHX2cTWhOMP/HFbzFg=="],

    "@remotion/studio": ["@remotion/studio@4.0.530", "", { "dependencies": { "@jridgewell/trace-mapping": "0.3.31", "@remotion/canvas": "4.0.530", "@remotion/captions": "4.0.530", "@remotion/codemods": "4.0.530", "@remotion/elevenlabs": "4.0.530", "@remotion/media": "4.0.530", "@remotion/media-utils": "4.0.530", "@remotion/openai-whisper": "4.0.530", "@remotion/paths": "4.0.530", "@remotion/player": "4.0.530", "@remotion/renderer": "4.0.530", "@remotion/studio-protocol": "4.0.530", "@remotion/studio-shared": "4.0.530", "@remotion/timeline-utils": "4.0.530", "@remotion/web-renderer": "4.0.530", "@remotion/zod-types": "4.0.530", "@tanstack/react-virtual": "3.14.9", "mediabunny": "1.56.1", "memfs": "3.4.3", "open": "8.4.2", "prismjs": "1.30.0", "remotion": "4.0.530", "semver": "7.5.3", "zod": "4.5.4" }, "peerDependencies": { "@remotion/video-matting": "4.0.530", "@remotion/whisper-webgpu": "4.0.530", "react": ">=16.8.0", "react-dom": ">=16.8.0" }, "optionalPeers": ["@remotion/video-matting", "@remotion/whisper-webgpu"] }, "sha512-Yki1b9nT3uWhVhzjASVH3AaWGEE4rqIRAoAHo67FCOgXSROpwWMNOc7AECPTsdVF8xyaI113hgYsACwsRv1ziQ=="],

    "@remotion/studio-protocol": ["@remotion/studio-protocol@4.0.530", "", { "dependencies": { "zod": "4.5.4" } }, "sha512-vHhvU0aKVFrQa7SWBFTEd9m2kiyZtgsf8dxzkO7h5JhzCyJBN1SGmxukjptt/ok5BFYWyixNBAnTyic12T3oww=="],

    "@remotion/studio-server": ["@remotion/studio-server@4.0.530", "", { "dependencies": { "@babel/parser": "7.24.1", "@babel/types": "7.24.0", "@remotion/bundler": "4.0.530", "@remotion/codemods": "4.0.530", "@remotion/renderer": "4.0.530", "@remotion/studio-protocol": "4.0.530", "@remotion/studio-shared": "4.0.530", "@svgr/core": "8.1.0", "@svgr/plugin-jsx": "8.1.0", "kiwi-schema": "0.5.0", "memfs": "3.4.3", "open": "8.4.2", "recast": "0.23.21", "remotion": "4.0.530", "semver": "7.5.3", "zod": "4.5.4" } }, "sha512-VCa1lh7/qyeW5UtXhU6g65RpCbjBYG0tDF4aY6zxCNjCLmQUUEHiDST/pGhnm1nCAT/bQW3SUynitrw5yn/Afg=="],

    "@remotion/studio-shared": ["@remotion/studio-shared@4.0.530", "", { "dependencies": { "remotion": "4.0.530" } }, "sha512-erBu4UhV+lYWf0BX+ZlHbiG5Wjn9fqyIqkMhypOyQHPVuQGw3I5sKw2dTOb8tuM9VejHFzcAtFvqkQmLRm3lNQ=="],

    "@remotion/timeline-utils": ["@remotion/timeline-utils@4.0.530", "", { "dependencies": { "mediabunny": "1.56.1", "remotion": "4.0.530" } }, "sha512-Ec81QAOY2fjm+td/jankYpjShU3zjfbsLybw2U4RGLEe4dpRXIz1KKvqsv7ExjG7MTxdiEzRXmJi7Ia+/b/nyQ=="],

    "@remotion/web-renderer": ["@remotion/web-renderer@4.0.530", "", { "dependencies": { "@mediabunny/aac-encoder": "1.56.1", "@mediabunny/flac-encoder": "1.56.1", "@mediabunny/mp3-encoder": "1.56.1", "@remotion/licensing": "4.0.530", "mediabunny": "1.56.1", "remotion": "4.0.530" }, "peerDependencies": { "react": ">=18.0.0", "react-dom": ">=18.0.0" } }, "sha512-10mD2X8+Bl2D08pRgN2ecJS1ENx8yCA7/lmjP9kJavuGa/e7QlbA76SD62/byTilzokSdx3VmSQrQjrRBExMng=="],

    "@remotion/zod-types": ["@remotion/zod-types@4.0.530", "", { "dependencies": { "remotion": "4.0.530" } }, "sha512-DfrQ7hMXAbDTR8xmKDHjbhdWo5z7aOTH8pGg/pmVY7wp5jXXOLyNHw3QeED14l7squ57tjR7z2gn0iDrsh3ptw=="],

    "@rspack/binding": ["@rspack/binding@1.7.11", "", { "optionalDependencies": { "@rspack/binding-darwin-arm64": "1.7.11", "@rspack/binding-darwin-x64": "1.7.11", "@rspack/binding-linux-arm64-gnu": "1.7.11", "@rspack/binding-linux-arm64-musl": "1.7.11", "@rspack/binding-linux-x64-gnu": "1.7.11", "@rspack/binding-linux-x64-musl": "1.7.11", "@rspack/binding-wasm32-wasi": "1.7.11", "@rspack/binding-win32-arm64-msvc": "1.7.11", "@rspack/binding-win32-ia32-msvc": "1.7.11", "@rspack/binding-win32-x64-msvc": "1.7.11" } }, "sha512-2MGdy2s2HimsDT444Bp5XnALzNRxuBNc7y0JzyuqKbHBywd4x2NeXyhWXXoxufaCFu5PBc9Qq9jyfjW2Aeh06Q=="],

    "@rspack/binding-darwin-arm64": ["@rspack/binding-darwin-arm64@1.7.11", "", { "os": "darwin", "cpu": "arm64" }, "sha512-oduECiZVqbO5zlVw+q7Vy65sJFth99fWPTyucwvLJJtJkPL5n17Uiql2cYP6Ijn0pkqtf1SXgK8WjiKLG5bIig=="],

    "@rspack/binding-darwin-x64": ["@rspack/binding-darwin-x64@1.7.11", "", { "os": "darwin", "cpu": "x64" }, "sha512-a1+TtTE9ap6RalgFi7FGIgkJP6O4Vy6ctv+9WGJy53E4kuqHR0RygzaiVxCI/GMc/vBT9vY23hyrpWb3d1vtXA=="],

    "@rspack/binding-linux-arm64-gnu": ["@rspack/binding-linux-arm64-gnu@1.7.11", "", { "os": "linux", "cpu": "arm64" }, "sha512-P0QrGRPbTWu6RKWfN0bDtbnEps3rXH0MWIMreZABoUrVmNQKtXR6e73J3ub6a+di5s2+K0M2LJ9Bh2/H4UsDUA=="],

    "@rspack/binding-linux-arm64-musl": ["@rspack/binding-linux-arm64-musl@1.7.11", "", { "os": "linux", "cpu": "arm64" }, "sha512-6ky7R43VMjWwmx3Yx7Jl7faLBBMAgMDt+/bN35RgwjiPgsIByz65EwytUVuW9rikB43BGHvA/eqlnjLrUzNBqw=="],

    "@rspack/binding-linux-x64-gnu": ["@rspack/binding-linux-x64-gnu@1.7.11", "", { "os": "linux", "cpu": "x64" }, "sha512-cuOJMfCOvb2Wgsry5enXJ3iT1FGUjdPqtGUBVupQlEG4ntSYsQ2PtF4wIDVasR3wdxC5nQbipOrDiN/u6fYsdQ=="],

    "@rspack/binding-linux-x64-musl": ["@rspack/binding-linux-x64-musl@1.7.11", "", { "os": "linux", "cpu": "x64" }, "sha512-CoK37hva4AmHGh3VCsQXmGr40L36m1/AdnN5LEjUX6kx5rEH7/1nEBN6Ii72pejqDVvk9anEROmPDiPw10tpFg=="],

    "@rspack/binding-wasm32-wasi": ["@rspack/binding-wasm32-wasi@1.7.11", "", { "dependencies": { "@napi-rs/wasm-runtime": "1.0.7" }, "cpu": "none" }, "sha512-OtrmnPUVJMxjNa3eDMfHyPdtlLRmmp/aIm0fQHlAOATbZvlGm12q7rhPW5BXTu1yh+1rQ1/uqvz+SzKEZXuJaQ=="],

    "@rspack/binding-win32-arm64-msvc": ["@rspack/binding-win32-arm64-msvc@1.7.11", "", { "os": "win32", "cpu": "arm64" }, "sha512-lObFW6e5lCWNgTBNwT//yiEDbsxm9QG4BYUojqeXxothuzJ/L6ibXz6+gLMvbOvLGV3nKgkXmx8GvT9WDKR0mA=="],

    "@rspack/binding-win32-ia32-msvc": ["@rspack/binding-win32-ia32-msvc@1.7.11", "", { "os": "win32", "cpu": "ia32" }, "sha512-0pYGnZd8PPqNR68zQ8skamqNAXEA1sUfXuAdYcknIIRq2wsbiwFzIc0Pov1cIfHYab37G7sSIPBiOUdOWF5Ivw=="],

    "@rspack/binding-win32-x64-msvc": ["@rspack/binding-win32-x64-msvc@1.7.11", "", { "os": "win32", "cpu": "x64" }, "sha512-EeQXayoQk/uBkI3pdoXfQBXNIUrADq56L3s/DFyM2pJeUDrWmhfIw2UFIGkYPTMSCo8F2JcdcGM32FGJrSnU0Q=="],

    "@rspack/core": ["@rspack/core@1.7.11", "", { "dependencies": { "@module-federation/runtime-tools": "0.22.0", "@rspack/binding": "1.7.11", "@rspack/lite-tapable": "1.1.0" }, "peerDependencies": { "@swc/helpers": ">=0.5.1" }, "optionalPeers": ["@swc/helpers"] }, "sha512-rsD9b+Khmot5DwCMiB3cqTQo53ioPG3M/A7BySu8+0+RS7GCxKm+Z+mtsjtG/vsu4Tn2tcqCdZtA3pgLoJB+ew=="],

    "@rspack/lite-tapable": ["@rspack/lite-tapable@1.1.0", "", {}, "sha512-E2B0JhYFmVAwdDiG14+DW0Di4Ze4Jg10Pc4/lILUrd5DRCaklduz2OvJ5HYQ6G+hd+WTzqQb3QnDNfK4yvAFYw=="],

    "@rspack/plugin-react-refresh": ["@rspack/plugin-react-refresh@1.6.1", "", { "dependencies": { "error-stack-parser": "^2.1.4", "html-entities": "^2.6.0" }, "peerDependencies": { "react-refresh": ">=0.10.0 <1.0.0", "webpack-hot-middleware": "2.x" }, "optionalPeers": ["webpack-hot-middleware"] }, "sha512-eqqW5645VG3CzGzFgNg5HqNdHVXY+567PGjtDhhrM8t67caxmsSzRmT5qfoEIfBcGgFkH9vEg7kzXwmCYQdQDw=="],

    "@svgr/babel-plugin-add-jsx-attribute": ["@svgr/babel-plugin-add-jsx-attribute@8.0.0", "", { "peerDependencies": { "@babel/core": "^7.0.0-0" } }, "sha512-b9MIk7yhdS1pMCZM8VeNfUlSKVRhsHZNMl5O9SfaX0l0t5wjdgu4IDzGB8bpnGBBOjGST3rRFVsaaEtI4W6f7g=="],

    "@svgr/babel-plugin-remove-jsx-attribute": ["@svgr/babel-plugin-remove-jsx-attribute@8.0.0", "", { "peerDependencies": { "@babel/core": "^7.0.0-0" } }, "sha512-BcCkm/STipKvbCl6b7QFrMh/vx00vIP63k2eM66MfHJzPr6O2U0jYEViXkHJWqXqQYjdeA9cuCl5KWmlwjDvbA=="],

    "@svgr/babel-plugin-remove-jsx-empty-expression": ["@svgr/babel-plugin-remove-jsx-empty-expression@8.0.0", "", { "peerDependencies": { "@babel/core": "^7.0.0-0" } }, "sha512-5BcGCBfBxB5+XSDSWnhTThfI9jcO5f0Ai2V24gZpG+wXF14BzwxxdDb4g6trdOux0rhibGs385BeFMSmxtS3uA=="],

    "@svgr/babel-plugin-replace-jsx-attribute-value": ["@svgr/babel-plugin-replace-jsx-attribute-value@8.0.0", "", { "peerDependencies": { "@babel/core": "^7.0.0-0" } }, "sha512-KVQ+PtIjb1BuYT3ht8M5KbzWBhdAjjUPdlMtpuw/VjT8coTrItWX6Qafl9+ji831JaJcu6PJNKCV0bp01lBNzQ=="],

    "@svgr/babel-plugin-svg-dynamic-title": ["@svgr/babel-plugin-svg-dynamic-title@8.0.0", "", { "peerDependencies": { "@babel/core": "^7.0.0-0" } }, "sha512-omNiKqwjNmOQJ2v6ge4SErBbkooV2aAWwaPFs2vUY7p7GhVkzRkJ00kILXQvRhA6miHnNpXv7MRnnSjdRjK8og=="],

    "@svgr/babel-plugin-svg-em-dimensions": ["@svgr/babel-plugin-svg-em-dimensions@8.0.0", "", { "peerDependencies": { "@babel/core": "^7.0.0-0" } }, "sha512-mURHYnu6Iw3UBTbhGwE/vsngtCIbHE43xCRK7kCw4t01xyGqb2Pd+WXekRRoFOBIY29ZoOhUCTEweDMdrjfi9g=="],

    "@svgr/babel-plugin-transform-react-native-svg": ["@svgr/babel-plugin-transform-react-native-svg@8.1.0", "", { "peerDependencies": { "@babel/core": "^7.0.0-0" } }, "sha512-Tx8T58CHo+7nwJ+EhUwx3LfdNSG9R2OKfaIXXs5soiy5HtgoAEkDay9LIimLOcG8dJQH1wPZp/cnAv6S9CrR1Q=="],

    "@svgr/babel-plugin-transform-svg-component": ["@svgr/babel-plugin-transform-svg-component@8.0.0", "", { "peerDependencies": { "@babel/core": "^7.0.0-0" } }, "sha512-DFx8xa3cZXTdb/k3kfPeaixecQLgKh5NVBMwD0AQxOzcZawK4oo1Jh9LbrcACUivsCA7TLG8eeWgrDXjTMhRmw=="],

    "@svgr/babel-preset": ["@svgr/babel-preset@8.1.0", "", { "dependencies": { "@svgr/babel-plugin-add-jsx-attribute": "8.0.0", "@svgr/babel-plugin-remove-jsx-attribute": "8.0.0", "@svgr/babel-plugin-remove-jsx-empty-expression": "8.0.0", "@svgr/babel-plugin-replace-jsx-attribute-value": "8.0.0", "@svgr/babel-plugin-svg-dynamic-title": "8.0.0", "@svgr/babel-plugin-svg-em-dimensions": "8.0.0", "@svgr/babel-plugin-transform-react-native-svg": "8.1.0", "@svgr/babel-plugin-transform-svg-component": "8.0.0" }, "peerDependencies": { "@babel/core": "^7.0.0-0" } }, "sha512-7EYDbHE7MxHpv4sxvnVPngw5fuR6pw79SkcrILHJ/iMpuKySNCl5W1qcwPEpU+LgyRXOaAFgH0KhwD18wwg6ug=="],

    "@svgr/core": ["@svgr/core@8.1.0", "", { "dependencies": { "@babel/core": "^7.21.3", "@svgr/babel-preset": "8.1.0", "camelcase": "^6.2.0", "cosmiconfig": "^8.1.3", "snake-case": "^3.0.4" } }, "sha512-8QqtOQT5ACVlmsvKOJNEaWmRPmcojMOzCz4Hs2BGG/toAp/K38LcsMRyLp349glq5AzJbCEeimEoxaX6v/fLrA=="],

    "@svgr/hast-util-to-babel-ast": ["@svgr/hast-util-to-babel-ast@8.0.0", "", { "dependencies": { "@babel/types": "^7.21.3", "entities": "^4.4.0" } }, "sha512-EbDKwO9GpfWP4jN9sGdYwPBU0kdomaPIL2Eu4YwmgP+sJeXT+L7bMwJUBnhzfH8Q2qMBqZ4fJwpCyYsAN3mt2Q=="],

    "@svgr/plugin-jsx": ["@svgr/plugin-jsx@8.1.0", "", { "dependencies": { "@babel/core": "^7.21.3", "@svgr/babel-preset": "8.1.0", "@svgr/hast-util-to-babel-ast": "8.0.0", "svg-parser": "^2.0.4" }, "peerDependencies": { "@svgr/core": "*" } }, "sha512-0xiIyBsLlr8quN+WyuxooNW9RJ0Dpr8uOnH/xrCVO8GLUcwHISwj1AG0k+LFzteTkAA0GbX0kj9q6Dk70PTiPA=="],

    "@tanstack/react-virtual": ["@tanstack/react-virtual@3.14.9", "", { "dependencies": { "@tanstack/virtual-core": "3.17.7" }, "peerDependencies": { "react": "^16.8.0 || ^17.0.0 || ^18.0.0 || ^19.0.0", "react-dom": "^16.8.0 || ^17.0.0 || ^18.0.0 || ^19.0.0" } }, "sha512-qZyr0FZDP8rDC4WBhsryIZmAd9bveJvFGUJJtskWaew6/0dTRS6wZxnR6VQ5bY2KwL3LjerrHqQLk3a0GKcPXQ=="],

    "@tanstack/virtual-core": ["@tanstack/virtual-core@3.17.7", "", {}, "sha512-bp+v10y65sp2H7WpWfIMyxTNfl8ZVfxFTLRjPIFRryi6FV/J33z4IS53WO4pTk36KlvJ4iLiQz+oaydDC1xbcA=="],

    "@tybys/wasm-util": ["@tybys/wasm-util@0.10.4", "", { "dependencies": { "tslib": "^2.4.0" } }, "sha512-W3c4gRigFS0T/Ma4qIYF3GDAc5AQdHb1yL5znJT1Zv1YaD9Kitx656wBjvr19qbiosmZT8lWDM5BEMynUqX65A=="],

    "@types/dom-mediacapture-transform": ["@types/dom-mediacapture-transform@0.1.12", "", { "dependencies": { "@types/dom-webcodecs": "*" } }, "sha512-d7/QsLRwF864A5mgIM/YrfiglHoYn7zgCcAoJgW404r+2DwnNr7EBbLnCWpmOMgH8y0te73L1AV6H1bmauaWFw=="],

    "@types/dom-webcodecs": ["@types/dom-webcodecs@0.1.13", "", {}, "sha512-O5hkiFIcjjszPIYyUSyvScyvrBoV3NOEEZx/pMlsu44TKzWNkLVBBxnxJz42in5n3QIolYOcBYFCPZZ0h8SkwQ=="],

    "@types/eslint": ["@types/eslint@9.6.1", "", { "dependencies": { "@types/estree": "*", "@types/json-schema": "*" } }, "sha512-FXx2pKgId/WyYo2jXw63kk7/+TY7u7AziEJxJAnSFzHlqTAS3Ync6SvgYAN/k4/PQpnnVuzoMuVnByKK2qp0ag=="],

    "@types/eslint-scope": ["@types/eslint-scope@3.7.7", "", { "dependencies": { "@types/eslint": "*", "@types/estree": "*" } }, "sha512-MzMFlSLBqNF2gcHWO0G1vP/YQyfvrxZ0bF+u7mzUdZ1/xK4A4sru+nraZz5i3iEIk1l1uyicaDVTB4QbbEkAYg=="],

    "@types/estree": ["@types/estree@1.0.9", "", {}, "sha512-GhdPgy1el4/ImP05X05Uw4cw2/M93BCUmnEvWZNStlCzEKME4Fkk+YpoA5OiHNQmoS7Cafb8Xa3Pya8m1Qrzeg=="],

    "@types/json-schema": ["@types/json-schema@7.0.15", "", {}, "sha512-5+fP8P8MFNC+AyZCDxrB2pkZFPGzqQWUzpSeuuVLvm8VMcorNYavBqoFcxK8bQz4Qsbn4oUEEem4wDLfcysGHA=="],

    "@types/node": ["@types/node@26.6.5", "", { "dependencies": { "undici-types": "~8.9.0" } }, "sha512-uMzsv9stDdofIZBx4UGh4Z9ZgXnGC9seRDscilBcTHAeOFk67MZg/k9bWVfO+bk4qZmG+l52hRnLwUiH2LnJTg=="],

    "@webassemblyjs/ast": ["@webassemblyjs/ast@1.14.1", "", { "dependencies": { "@webassemblyjs/helper-numbers": "1.13.2", "@webassemblyjs/helper-wasm-bytecode": "1.13.2" } }, "sha512-nuBEDgQfm1ccRp/8bCQrx1frohyufl4JlbMMZ4P1wpeOfDhF6FQkxZJ1b/e+PLwr6X1Nhw6OLme5usuBWYBvuQ=="],

    "@webassemblyjs/floating-point-hex-parser": ["@webassemblyjs/floating-point-hex-parser@1.13.2", "", {}, "sha512-6oXyTOzbKxGH4steLbLNOu71Oj+C8Lg34n6CqRvqfS2O71BxY6ByfMDRhBytzknj9yGUPVJ1qIKhRlAwO1AovA=="],

    "@webassemblyjs/helper-api-error": ["@webassemblyjs/helper-api-error@1.13.2", "", {}, "sha512-U56GMYxy4ZQCbDZd6JuvvNV/WFildOjsaWD3Tzzvmw/mas3cXzRJPMjP83JqEsgSbyrmaGjBfDtV7KDXV9UzFQ=="],

    "@webassemblyjs/helper-buffer": ["@webassemblyjs/helper-buffer@1.14.1", "", {}, "sha512-jyH7wtcHiKssDtFPRB+iQdxlDf96m0E39yb0k5uJVhFGleZFoNw1c4aeIcVUPPbXUVJ94wwnMOAqUHyzoEPVMA=="],

    "@webassemblyjs/helper-numbers": ["@webassemblyjs/helper-numbers@1.13.2", "", { "dependencies": { "@webassemblyjs/floating-point-hex-parser": "1.13.2", "@webassemblyjs/helper-api-error": "1.13.2", "@xtuc/long": "4.2.2" } }, "sha512-FE8aCmS5Q6eQYcV3gI35O4J789wlQA+7JrqTTpJqn5emA4U2hvwJmvFRC0HODS+3Ye6WioDklgd6scJ3+PLnEA=="],

    "@webassemblyjs/helper-wasm-bytecode": ["@webassemblyjs/helper-wasm-bytecode@1.13.2", "", {}, "sha512-3QbLKy93F0EAIXLh0ogEVR6rOubA9AoZ+WRYhNbFyuB70j3dRdwH9g+qXhLAO0kiYGlg3TxDV+I4rQTr/YNXkA=="],

    "@webassemblyjs/helper-wasm-section": ["@webassemblyjs/helper-wasm-section@1.14.1", "", { "dependencies": { "@webassemblyjs/ast": "1.14.1", "@webassemblyjs/helper-buffer": "1.14.1", "@webassemblyjs/helper-wasm-bytecode": "1.13.2", "@webassemblyjs/wasm-gen": "1.14.1" } }, "sha512-ds5mXEqTJ6oxRoqjhWDU83OgzAYjwsCV8Lo/N+oRsNDmx/ZDpqalmrtgOMkHwxsG0iI//3BwWAErYRHtgn0dZw=="],

    "@webassemblyjs/ieee754": ["@webassemblyjs/ieee754@1.13.2", "", { "dependencies": { "@xtuc/ieee754": "^1.2.0" } }, "sha512-4LtOzh58S/5lX4ITKxnAK2USuNEvpdVV9AlgGQb8rJDHaLeHciwG4zlGr0j/SNWlr7x3vO1lDEsuePvtcDNCkw=="],

    "@webassemblyjs/leb128": ["@webassemblyjs/leb128@1.13.2", "", { "dependencies": { "@xtuc/long": "4.2.2" } }, "sha512-Lde1oNoIdzVzdkNEAWZ1dZ5orIbff80YPdHx20mrHwHrVNNTjNr8E3xz9BdpcGqRQbAEa+fkrCb+fRFTl/6sQw=="],

    "@webassemblyjs/utf8": ["@webassemblyjs/utf8@1.13.2", "", {}, "sha512-3NQWGjKTASY1xV5m7Hr0iPeXD9+RDobLll3T9d2AO+g3my8xy5peVyjSag4I50mR1bBSN/Ct12lo+R9tJk0NZQ=="],

    "@webassemblyjs/wasm-edit": ["@webassemblyjs/wasm-edit@1.14.1", "", { "dependencies": { "@webassemblyjs/ast": "1.14.1", "@webassemblyjs/helper-buffer": "1.14.1", "@webassemblyjs/helper-wasm-bytecode": "1.13.2", "@webassemblyjs/helper-wasm-section": "1.14.1", "@webassemblyjs/wasm-gen": "1.14.1", "@webassemblyjs/wasm-opt": "1.14.1", "@webassemblyjs/wasm-parser": "1.14.1", "@webassemblyjs/wast-printer": "1.14.1" } }, "sha512-RNJUIQH/J8iA/1NzlE4N7KtyZNHi3w7at7hDjvRNm5rcUXa00z1vRz3glZoULfJ5mpvYhLybmVcwcjGrC1pRrQ=="],

    "@webassemblyjs/wasm-gen": ["@webassemblyjs/wasm-gen@1.14.1", "", { "dependencies": { "@webassemblyjs/ast": "1.14.1", "@webassemblyjs/helper-wasm-bytecode": "1.13.2", "@webassemblyjs/ieee754": "1.13.2", "@webassemblyjs/leb128": "1.13.2", "@webassemblyjs/utf8": "1.13.2" } }, "sha512-AmomSIjP8ZbfGQhumkNvgC33AY7qtMCXnN6bL2u2Js4gVCg8fp735aEiMSBbDR7UQIj90n4wKAFUSEd0QN2Ukg=="],

    "@webassemblyjs/wasm-opt": ["@webassemblyjs/wasm-opt@1.14.1", "", { "dependencies": { "@webassemblyjs/ast": "1.14.1", "@webassemblyjs/helper-buffer": "1.14.1", "@webassemblyjs/wasm-gen": "1.14.1", "@webassemblyjs/wasm-parser": "1.14.1" } }, "sha512-PTcKLUNvBqnY2U6E5bdOQcSM+oVP/PmrDY9NzowJjislEjwP/C4an2303MCVS2Mg9d3AJpIGdUFIQQWbPds0Sw=="],

    "@webassemblyjs/wasm-parser": ["@webassemblyjs/wasm-parser@1.14.1", "", { "dependencies": { "@webassemblyjs/ast": "1.14.1", "@webassemblyjs/helper-api-error": "1.13.2", "@webassemblyjs/helper-wasm-bytecode": "1.13.2", "@webassemblyjs/ieee754": "1.13.2", "@webassemblyjs/leb128": "1.13.2", "@webassemblyjs/utf8": "1.13.2" } }, "sha512-JLBl+KZ0R5qB7mCnud/yyX08jWFw5MsoalJ1pQ4EdFlgj9VdXKGuENGsiCIjegI1W7p91rUlcB/LB5yRJKNTcQ=="],

    "@webassemblyjs/wast-printer": ["@webassemblyjs/wast-printer@1.14.1", "", { "dependencies": { "@webassemblyjs/ast": "1.14.1", "@xtuc/long": "4.2.2" } }, "sha512-kPSSXE6De1XOR820C90RIo2ogvZG+c3KiHzqUoO/F34Y2shGzesfqv7o57xrxovZJH/MetF5UjroJ/R/3isoiw=="],

    "@xtuc/ieee754": ["@xtuc/ieee754@1.2.0", "", {}, "sha512-DX8nKgqcGwsc0eJSqYt5lwP4DH5FlHnmuWWBRy7X0NcaGR0ZtuyeESgMwTYVEtxmsNGY+qit4QYT/MIYTOTPeA=="],

    "@xtuc/long": ["@xtuc/long@4.2.2", "", {}, "sha512-NuHqBY1PB/D8xU6s/thBgOAiAP7HOYDQ32+BFZILJ8ivkUkAHQnWfn6WhL79Owj1qmUnoN/YPhktdIoucipkAQ=="],

    "acorn": ["acorn@8.19.0", "", { "bin": { "acorn": "bin/acorn" } }, "sha512-oJlA3XiRm7Cyk6qFD2Jn8ak9B7jSy0qy00ADO3+8dpT0LSjFihQYv4C02LFCSYJV3Q37xYwwRy5m+IpIiUzqWw=="],

    "acorn-import-phases": ["acorn-import-phases@1.0.4", "", { "peerDependencies": { "acorn": "^8.14.0" } }, "sha512-wKmbr/DDiIXzEOiWrTTUcDm24kQ2vGfZQvM2fwg2vXqR5uW6aapr7ObPtj1th32b9u90/Pf4AItvdTh42fBmVQ=="],

    "ajv": ["ajv@8.20.0", "", { "dependencies": { "fast-deep-equal": "^3.1.3", "fast-uri": "^3.0.1", "json-schema-traverse": "^1.0.0", "require-from-string": "^2.0.2" } }, "sha512-Thbli+OlOj+iMPYFBVBfJ3OmCAnaSyNn4M1vz9T6Gka5Jt9ba/HIR56joy65tY6kx/FCF5VXNB819Y7/GUrBGA=="],

    "ajv-formats": ["ajv-formats@3.0.1", "", { "dependencies": { "ajv": "^8.0.0" } }, "sha512-8iUql50EUR+uUcdRQ3HDqa6EVyo3docL8g5WJ3FNcWmu62IbkGUue/pEyLBW8VGKKucTPgqeks4fIU1DA4yowQ=="],

    "ajv-keywords": ["ajv-keywords@5.1.0", "", { "dependencies": { "fast-deep-equal": "^3.1.3" }, "peerDependencies": { "ajv": "^8.8.2" } }, "sha512-YCS/JNFAUyr5vAuhk1DWm1CBxRHW9LbJ2ozWeemrIqpbsqKjHVxYPyi5GC0rjZIT5JxJ3virVTS8wk4i/Z+krw=="],

    "argparse": ["argparse@2.0.1", "", {}, "sha512-8+9WqebbFzpX9OR+Wa6O29asIogeRMzcGtAINdpMHHyAg10f05aSFVBbcEqGf/PXw1EjAZ+q2/bEBg3DvurK3Q=="],

    "ast-types": ["ast-types@0.16.1", "", { "dependencies": { "tslib": "^2.0.1" } }, "sha512-6t10qk83GOG8p0vKmaCr8eiilZwO171AvbROMtvvNiwrTly62t+7XkA8RdIIVbpMhCASAsxgAzdRSwh6nw/5Dg=="],

    "baseline-browser-mapping": ["baseline-browser-mapping@2.11.28", "", { "bin": { "baseline-browser-mapping": "dist/cli.cjs" } }, "sha512-br0LOmjJqr6Rt4AEkadbcNf67Zpo7EPwKsWbjnRrJIa1QYFHQBqM4C7F2WTbV8ahTEcg1Eo+Y0aWjjORInYFyA=="],

    "browserslist": ["browserslist@4.29.3", "", { "dependencies": { "baseline-browser-mapping": "^2.11.26", "caniuse-lite": "^1.0.30001813", "electron-to-chromium": "^1.5.439", "node-releases": "^2.0.57", "update-browserslist-db": "^1.3.3" }, "bin": { "browserslist": "cli.js" } }, "sha512-1R4kiYKXGViqEN0CnoDrXc1StD9niAwu+j2dukWzrD4bJgsD4lDmEp0CRbc6E/vYJIfTHwPmwyaKtVSudICdPA=="],

    "buffer-from": ["buffer-from@1.1.2", "", {}, "sha512-E+XQCRwSbaaiChtv6k6Dwgc+bx+Bs6vuKJHHl5kox/BaKbhiXzqQOwK4cO22yElGp2OCmjwVhT3HmxgyPGnJfQ=="],

    "callsites": ["callsites@3.1.0", "", {}, "sha512-P8BjAsXvZS+VIDUI11hHCQEv74YT67YUi5JJFNWIqL235sBmjX4+qx9Muvls5ivyNENctx46xQLQ3aTuE7ssaQ=="],

    "camelcase": ["camelcase@6.3.0", "", {}, "sha512-Gmy6FhYlCY7uOElZUSbxo2UCDH8owEk996gkbrpsgGtrJLM3J7jGxl9Ic7Qwwj4ivOE5AWZWRMecDdF7hqGjFA=="],

    "caniuse-lite": ["caniuse-lite@1.0.30001816", "", {}, "sha512-+8Yx7BXCoqk6IF8yTicjfUR6D/ldJzdlsodlEOiOSPmhK844WIgk67/zIQaGAOxNkZyyvBlrRFnLvqKIoqbAFw=="],

    "chrome-trace-event": ["chrome-trace-event@1.0.4", "", {}, "sha512-rNjApaLzuwaOTjCiT8lSDdGN1APCiqkChLMJxJPWLunPAt5fy8xgU9/jNOchV84wfIxrA0lRQB7oCT8jrn/wrQ=="],

    "commander": ["commander@2.20.3", "", {}, "sha512-GpVkmM8vF2vQUkj2LvZmD35JxeJOLCwJ9cUkugyk2nuhbv3+mJvpLYYt+0+USMxE+oj+ey/lJEnhZw75x/OMcQ=="],

    "convert-source-map": ["convert-source-map@2.0.0", "", {}, "sha512-Kvp459HrV2FEJ1CAsi1Ku+MY3kasH19TFykTz2xWmMeq6bk2NU3XXvfJ+Q61m0xktWwt+1HSYf3JZsTms3aRJg=="],

    "cosmiconfig": ["cosmiconfig@8.3.6", "", { "dependencies": { "import-fresh": "^3.3.0", "js-yaml": "^4.1.0", "parse-json": "^5.2.0", "path-type": "^4.0.0" }, "peerDependencies": { "typescript": ">=4.9.5" }, "optionalPeers": ["typescript"] }, "sha512-kcZ6+W5QzcJ3P1Mt+83OUv/oHFqZHIx8DuxG6eZ5RGMERoLqp4BuGjhHLYGK+Kf5XVkQvqBSmAy/nGWN3qDgEA=="],

    "cross-spawn": ["cross-spawn@7.0.6", "", { "dependencies": { "path-key": "^3.1.0", "shebang-command": "^2.0.0", "which": "^2.0.1" } }, "sha512-uV2QOWP2nWzsy2aMp8aRibhi9dlzF5Hgh5SHaB9OiTGEyDTiJJyx0uy51QXdyWbtAHNua4XJzUKca3OzKUd3vA=="],

    "css-loader": ["css-loader@7.1.4", "", { "dependencies": { "icss-utils": "^5.1.0", "postcss": "^8.4.40", "postcss-modules-extract-imports": "^3.1.0", "postcss-modules-local-by-default": "^4.0.5", "postcss-modules-scope": "^3.2.0", "postcss-modules-values": "^4.0.0", "postcss-value-parser": "^4.2.0", "semver": "^7.6.3" }, "peerDependencies": { "@rspack/core": "0.x || ^1.0.0 || ^2.0.0-0", "webpack": "^5.27.0" }, "optionalPeers": ["@rspack/core", "webpack"] }, "sha512-vv3J9tlOl04WjiMvHQI/9tmIrCxVrj6PFbHemBB1iihpeRbi/I4h033eoFIhwxBBqLhI0KYFS7yvynBFhIZfTw=="],

    "cssesc": ["cssesc@3.0.0", "", { "bin": { "cssesc": "bin/cssesc" } }, "sha512-/Tb/JcjK111nNScGob5MNtsntNM1aCNUDipB/TkwZFhyDrrE47SOx/18wF2bbjgc3ZzCSKW1T5nt5EbFoAz/Vg=="],

    "debug": ["debug@4.4.3", "", { "dependencies": { "ms": "^2.1.3" }, "peerDependencies": { "supports-color": "*" }, "optionalPeers": ["supports-color"] }, "sha512-RGwwWnwQvkVfavKVt22FGLw+xYSdzARwm0ru6DhTVA3umU5hZc28V3kO4stgYryrTlLpuvgI9GiijltAjNbcqA=="],

    "define-lazy-prop": ["define-lazy-prop@2.0.0", "", {}, "sha512-Ds09qNh8yw3khSjiJjiUInaGX9xlqZDY7JVryGxdxV7NPeuqQfplOpQ66yJFZut3jLa5zOwkXw1g9EI2uKh4Og=="],

    "dot-case": ["dot-case@3.0.4", "", { "dependencies": { "no-case": "^3.0.4", "tslib": "^2.0.3" } }, "sha512-Kv5nKlh6yRrdrGvxeJ2e5y2eRUpkUosIW4A2AS38zwSz27zu7ufDwQPi5Jhs3XAlGNetl3bmnGhQsMtkKJnj3w=="],

    "dotenv": ["dotenv@17.3.1", "", {}, "sha512-IO8C/dzEb6O3F9/twg6ZLXz164a2fhTnEWb95H23Dm4OuN+92NmEAlTrupP9VW6Jm3sO26tQlqyvyi4CsnY9GA=="],

    "electron-to-chromium": ["electron-to-chromium@1.5.456", "", {}, "sha512-8hboqI6xesozteFb8aa7OGknvxUtTeRJLz0FoePysUEh/oWbddykIGdgpEJRbPRg/nIMfBf2DFos+H2MtvJl2A=="],

    "enhanced-resolve": ["enhanced-resolve@5.26.0", "", { "dependencies": { "graceful-fs": "^4.2.4", "tapable": "^2.3.3" } }, "sha512-9vhedylFonb2YGogzUKX6+Ja72gOJbN1QHAqdrvqLwhdl/QWbKopzoUC9EbQNVsAns/bx/4uyqalrQAoy1IByw=="],

    "entities": ["entities@4.5.0", "", {}, "sha512-V0hjH4dGPh9Ao5p0MoRY6BVqtwCjhz6vI5LT8AJ55H+4g9/4vbHx1I54fS0XuclLhDHArPQCiMjDxjaL8fPxhw=="],

    "error-ex": ["error-ex@1.3.4", "", { "dependencies": { "is-arrayish": "^0.2.1" } }, "sha512-sqQamAnR14VgCr1A618A3sGrygcpK+HEbenA/HiEAkkUwcZIIB/tgWqHFxWgOyDh4nB4JCRimh79dR5Ywc9MDQ=="],

    "error-stack-parser": ["error-stack-parser@2.1.4", "", { "dependencies": { "stackframe": "^1.3.4" } }, "sha512-Sk5V6wVazPhq5MhpO+AUxJn5x7XSXGl1R93Vn7i+zS15KDVxQijejNCrz8340/2bgLBjR9GtEG8ZVKONDjcqGQ=="],

    "es-module-lexer": ["es-module-lexer@2.3.2", "", {}, "sha512-poHGpORABojJJucnV9KbOavETW8lBVnphkW77ER5/BQ5Fz7oXSoCNek7IH3vR5nRjdsEz926ibFYX8KtLQmdyw=="],

    "esbuild": ["esbuild@0.28.1", "", { "optionalDependencies": { "@esbuild/aix-ppc64": "0.28.1", "@esbuild/android-arm": "0.28.1", "@esbuild/android-arm64": "0.28.1", "@esbuild/android-x64": "0.28.1", "@esbuild/darwin-arm64": "0.28.1", "@esbuild/darwin-x64": "0.28.1", "@esbuild/freebsd-arm64": "0.28.1", "@esbuild/freebsd-x64": "0.28.1", "@esbuild/linux-arm": "0.28.1", "@esbuild/linux-arm64": "0.28.1", "@esbuild/linux-ia32": "0.28.1", "@esbuild/linux-loong64": "0.28.1", "@esbuild/linux-mips64el": "0.28.1", "@esbuild/linux-ppc64": "0.28.1", "@esbuild/linux-riscv64": "0.28.1", "@esbuild/linux-s390x": "0.28.1", "@esbuild/linux-x64": "0.28.1", "@esbuild/netbsd-arm64": "0.28.1", "@esbuild/netbsd-x64": "0.28.1", "@esbuild/openbsd-arm64": "0.28.1", "@esbuild/openbsd-x64": "0.28.1", "@esbuild/openharmony-arm64": "0.28.1", "@esbuild/sunos-x64": "0.28.1", "@esbuild/win32-arm64": "0.28.1", "@esbuild/win32-ia32": "0.28.1", "@esbuild/win32-x64": "0.28.1" }, "bin": { "esbuild": "bin/esbuild" } }, "sha512-HrJrvZv5ayxBzPfwphOoNzkzOIIlifzk0KJrGK2c8R4+LKpMtpYLQeUdjnwjWv/LZlkH2laZk+4w78pi99D4Vw=="],

    "escalade": ["escalade@3.2.0", "", {}, "sha512-WUj2qlxaQtO4g6Pq5c29GTcWGDyd8itL8zTlipgECz3JesAiiOKotd8JU6otB3PACgG6xkJUyVhboMS+bje/jA=="],

    "eslint-scope": ["eslint-scope@5.1.1", "", { "dependencies": { "esrecurse": "^4.3.0", "estraverse": "^4.1.1" } }, "sha512-2NxwbF/hZ0KpepYN0cNbo+FN6XoK7GaHlQhgx/hIZl6Va0bF45RQOOwhLIy8lQDbuCiadSLCBnH2CFYquit5bw=="],

    "esprima": ["esprima@4.0.1", "", { "bin": { "esparse": "./bin/esparse.js", "esvalidate": "./bin/esvalidate.js" } }, "sha512-eGuFFw7Upda+g4p+QHvnW0RyTX/SVeJBDM/gCtMARO0cLuT2HcEKnTPvhjV6aGeqrCB/sbNop0Kszm0jsaWU4A=="],

    "esrecurse": ["esrecurse@4.3.0", "", { "dependencies": { "estraverse": "^5.2.0" } }, "sha512-KmfKL3b6G+RXvP8N1vr3Tq1kL/oCFgn2NYXEtqP8/L3pKapUA4G8cFVaoF3SU323CD4XypR/ffioHmkti6/Tag=="],

    "estraverse": ["estraverse@4.3.0", "", {}, "sha512-39nnKffWz8xN1BU/2c79n9nB9HDzo0niYUqx6xyqUnyoAnQyyWpOTdZEeiCch8BBu515t4wp9ZmgVfVhn9EBpw=="],

    "events": ["events@3.3.0", "", {}, "sha512-mQw+2fkQbALzQ7V0MY0IqdnXNOeTtP4r0lN9z7AAawCXgqea7bDii20AYrIBrFd/Hx0M2Ocz6S111CaFkUcb0Q=="],

    "execa": ["execa@5.1.1", "", { "dependencies": { "cross-spawn": "^7.0.3", "get-stream": "^6.0.0", "human-signals": "^2.1.0", "is-stream": "^2.0.0", "merge-stream": "^2.0.0", "npm-run-path": "^4.0.1", "onetime": "^5.1.2", "signal-exit": "^3.0.3", "strip-final-newline": "^2.0.0" } }, "sha512-8uSpZZocAZRBAPIEINJj3Lo9HyGitllczc27Eh5YYojjMFMn8yHMDMaUHE2Jqfq05D/wucwI4JGURyXt1vchyg=="],

    "fast-deep-equal": ["fast-deep-equal@3.1.3", "", {}, "sha512-f3qQ9oQy9j2AhBe/H9VC91wLmKBCCU/gDOnKNAYG5hswO7BLKj09Hc5HYNz9cGI++xlpDCIgDaitVs03ATR84Q=="],

    "fast-uri": ["fast-uri@3.1.8", "", {}, "sha512-GZMtZUTNRpOVIECoXwLNZS5xUGE+mVNbTB8h/7Rwh2TFWcBQiPzTgyZi05BF9UMZKkLJv8XBRJTlU7zg8+ZfMg=="],

    "fs-monkey": ["fs-monkey@1.0.3", "", {}, "sha512-cybjIfiiE+pTWicSCLFHSrXZ6EilF30oh91FDP9S2B051prEa7QWfrVTQm10/dDpswBDXZugPa1Ogu8Yh+HV0Q=="],

    "gensync": ["gensync@1.0.0-beta.2", "", {}, "sha512-3hN7NaskYvMDLQY55gnW3NQ+mesEAepTqlg+VEbj7zzqEMBVNhzcGYYeqFo/TlYz6eQiFcp1HcsCZO+nGgS8zg=="],

    "get-stream": ["get-stream@6.0.1", "", {}, "sha512-ts6Wi+2j3jQjqi70w5AlN8DFnkSwC+MqmxEzdEALB2qXZYV3X/b1CTfgPLGJNMeAWxdPfU8FO1ms3NUfaHCPYg=="],

    "glob-to-regexp": ["glob-to-regexp@0.4.1", "", {}, "sha512-lkX1HJXwyMcprw/5YUZc2s7DrpAiHB21/V+E1rHUrVNokkvB6bqMzT0VfV6/86ZNabt1k14YOIaT7nDvOX3Iiw=="],

    "graceful-fs": ["graceful-fs@4.2.11", "", {}, "sha512-RbJ5/jmFcNNCcDV5o9eTnBLJ/HszWV0P73bc+Ff4nS/rJj+YaS6IGyiOL0VoBYX+l1Wrl3k63h/KrH+nhJ0XvQ=="],

    "has-flag": ["has-flag@4.0.0", "", {}, "sha512-EykJT/Q1KjTWctppgIAgfSO0tKVuZUjhgMr17kqTumMl6Afv3EISleU7qZUzoXDFTAHTDC4NOoG/ZxU3EvlMPQ=="],

    "html-entities": ["html-entities@2.6.0", "", {}, "sha512-kig+rMn/QOVRvr7c86gQ8lWXq+Hkv6CbAH1hLu+RG338StTpE8Z0b44SDVaqVu7HGKf27frdmUYEs9hTUX/cLQ=="],

    "human-signals": ["human-signals@2.1.0", "", {}, "sha512-B4FFZ6q/T2jhhksgkbEW3HBvWIfDW85snkQgawt07S7J5QXTk6BkNV+0yAeZrM5QpMAdYlocGoljn0sJ/WQkFw=="],

    "icss-utils": ["icss-utils@5.1.0", "", { "peerDependencies": { "postcss": "^8.1.0" } }, "sha512-soFhflCVWLfRNOPU3iv5Z9VUdT44xFRbzjLsEzSr5AQmgqPMTHdU3PMT1Cf1ssx8fLNJDA1juftYl+PUcv3MqA=="],

    "import-fresh": ["import-fresh@3.3.1", "", { "dependencies": { "parent-module": "^1.0.0", "resolve-from": "^4.0.0" } }, "sha512-TR3KfrTZTYLPB6jUjfx6MF9WcWrHL9su5TObK4ZkYgBdWKPOFoSoQIdEuTuR82pmtxH2spWG9h6etwfr1pLBqQ=="],

    "is-arrayish": ["is-arrayish@0.2.1", "", {}, "sha512-zz06S8t0ozoDXMG+ube26zeCTNXcKIPJZJi8hBrF4idCLms4CG9QtK7qBl1boi5ODzFpjswb5JPmHCbMpjaYzg=="],

    "is-docker": ["is-docker@2.2.1", "", { "bin": { "is-docker": "cli.js" } }, "sha512-F+i2BKsFrH66iaUFc0woD8sLy8getkwTwtOBjvs56Cx4CgJDeKQeqfz8wAYiSb8JOprWhHH5p77PbmYCvvUuXQ=="],

    "is-stream": ["is-stream@2.0.1", "", {}, "sha512-hFoiJiTl63nn+kstHGBtewWSKnQLpyb155KHheA1l39uvtO9nWIop1p3udqPcUd/xbF1VLMO4n7OI6p7RbngDg=="],

    "is-wsl": ["is-wsl@2.2.0", "", { "dependencies": { "is-docker": "^2.0.0" } }, "sha512-fKzAra0rGJUUBwGBgNkHZuToZcn+TtXHpeCgmkMJMMYx1sQDYaCSyjJBSCa2nH1DGm7s3n1oBnohoVTBaN7Lww=="],

    "isexe": ["isexe@2.0.0", "", {}, "sha512-RHxMLp9lnKHGHRng9QFhRCMbYAcVpn69smSGcq3f36xjgVVWThj4qqLbTLlq7Ssj8B+fIQ1EuCEGI2lKsyQeIw=="],

    "jest-worker": ["jest-worker@27.5.1", "", { "dependencies": { "@types/node": "*", "merge-stream": "^2.0.0", "supports-color": "^8.0.0" } }, "sha512-7vuh85V5cdDofPyxn58nrPjBktZo0u9x1g8WtjQol+jZDaE+fhN+cIvTj11GndBnMnyfrUOG1sZQxCdjKh+DKg=="],

    "js-tokens": ["js-tokens@4.0.0", "", {}, "sha512-RdJUflcE3cUzKiMqQgsCu06FPu9UdIJO0beYbPhHN4k6apgJtifcoCtT9bcxOpYBtpD2kCM6Sbzg4CausW/PKQ=="],

    "js-yaml": ["js-yaml@4.3.2", "", { "dependencies": { "argparse": "^2.0.1" }, "bin": { "js-yaml": "bin/js-yaml.js" } }, "sha512-SFNOvSJ+Dgf/9An904Yx+CgSlIPCkIpao4qo51lpee25TIRejdH3rhR4EZMGoNx3/TP3O+wzWuiTFl4sqbltzA=="],

    "jsesc": ["jsesc@3.1.0", "", { "bin": { "jsesc": "bin/jsesc" } }, "sha512-/sM3dO2FOzXjKQhJuo0Q173wf2KOo8t4I8vHy6lF9poUp7bKT0/NHE8fPX23PwfhnykfqnC2xRxOnVw5XuGIaA=="],

    "json-parse-even-better-errors": ["json-parse-even-better-errors@2.3.1", "", {}, "sha512-xyFwyhro/JEof6Ghe2iz2NcXoj2sloNsWr/XsERDK/oiPCfaNhl5ONfp+jQdAZRQQ0IJWNzH9zIZF7li91kh2w=="],

    "json-schema-traverse": ["json-schema-traverse@1.0.0", "", {}, "sha512-NM8/P9n3XjXhIZn1lLhkFaACTOURQXjWhV4BA/RnOv8xvgqtqpAX9IO4mRQxSx1Rlo4tqzeqb0sOlruaOy3dug=="],

    "json5": ["json5@2.2.3", "", { "bin": { "json5": "lib/cli.js" } }, "sha512-XmOWe7eyHYH14cLdVPoyg+GOH3rYX++KpzrylJwSW98t3Nk+U8XOl8FWKOgwtzdb8lXGf6zYwDUzeHMWfxasyg=="],

    "kiwi-schema": ["kiwi-schema@0.5.0", "", { "bin": { "kiwic": "cli.js" } }, "sha512-X+FpfU0yTEtc6aTHS7VwbOpvQwRt70+pXXWRI5fd6CvWhe7pSVC854TVo4Zo0x5/wwcWj+/9KUlXpdcP0dY9AA=="],

    "kleur": ["kleur@3.0.3", "", {}, "sha512-eTIzlVOSUR+JxdDFepEYcBMtZ9Qqdef+rnzWdRZuMbOywu5tO2w2N7rqjoANZ5k9vywhL6Br1VRjUIgTQx4E8w=="],

    "lines-and-columns": ["lines-and-columns@1.2.4", "", {}, "sha512-7ylylesZQ/PV29jhEDl3Ufjo6ZX7gCqJr5F7PKrqc93v7fzSymt1BpwEU8nAUXs8qzzvqhbjhK5QZg6Mt/HkBg=="],

    "loader-runner": ["loader-runner@4.3.2", "", {}, "sha512-DFEqQ3ihfS9blba08cLfYf1NRAIEm+dDjic073DRDc3/JspI/8wYmtDsHwd3+4hwvdxSK7PGaElfTmm0awWJ4w=="],

    "loose-envify": ["loose-envify@1.4.0", "", { "dependencies": { "js-tokens": "^3.0.0 || ^4.0.0" }, "bin": { "loose-envify": "cli.js" } }, "sha512-lyuxPGr/Wfhrlem2CL/UcnUc1zcqKAImBDzukY7Y5F/yQiNdko6+fRLevlw1HgMySw7f611UIY408EtxRSoK3Q=="],

    "lower-case": ["lower-case@2.0.2", "", { "dependencies": { "tslib": "^2.0.3" } }, "sha512-7fm3l3NAF9WfN6W3JOmf5drwpVqX78JtoGJ3A6W0a6ZnldM41w2fV5D490psKFTpMds8TJse/eHLFFsNHHjHgg=="],

    "lru-cache": ["lru-cache@6.0.0", "", { "dependencies": { "yallist": "^4.0.0" } }, "sha512-Jo6dJ04CmSjuznwJSS3pUeWmd/H0ffTlkXXgwZi+eq1UCmqQwCh+eLsYOYCwY991i2Fah4h1BEMCx4qThGbsiA=="],

    "mediabunny": ["mediabunny@1.56.1", "", { "dependencies": { "@types/dom-mediacapture-transform": "^0.1.11", "@types/dom-webcodecs": "0.1.13" } }, "sha512-DNOm0bRBmeOxJgCK/g3LxNWbxY5morTauNdlychujGmJ9L37ezVezkNoI1WtO2Xdb4WlWWJlYfIKnOEzd5phRw=="],

    "memfs": ["memfs@3.4.3", "", { "dependencies": { "fs-monkey": "1.0.3" } }, "sha512-eivjfi7Ahr6eQTn44nvTnR60e4a1Fs1Via2kCR5lHo/kyNoiMWaXCNJ/GpSd0ilXas2JSOl9B5FTIhflXu0hlg=="],

    "merge-stream": ["merge-stream@2.0.0", "", {}, "sha512-abv/qOcuPfk3URPfDzmZU1LKmuw8kT+0nIHvKrKgFrwifol/doWcdA4ZqsWQ8ENrFKkd67Mfpo/LovbIUsbt3w=="],

    "mime-db": ["mime-db@1.52.0", "", {}, "sha512-sPU4uV7dYlvtWJxwwxHD0PuihVNiE7TyAbQ5SWxDCB9mUYvOgroQOwYQQOKPJ8CIbE+1ETVlOoK1UC2nU3gYvg=="],

    "mime-types": ["mime-types@2.1.35", "", { "dependencies": { "mime-db": "1.52.0" } }, "sha512-ZDY+bPm5zTTF+YpCrAU9nK0UgICYPT0QtT1NZWFv4s++TNkcgVaT0g6+4R2uI4MjQjzysHB1zxuWL50hzaeXiw=="],

    "mimic-fn": ["mimic-fn@2.1.0", "", {}, "sha512-OqbOk5oEQeAZ8WXWydlu9HJjz9WVdEIvamMCcXmuqUYjTknH/sqsWvhQ3vgwKFRR1HpjvNBKQ37nbJgYzGqGcg=="],

    "minimist": ["minimist@1.2.6", "", {}, "sha512-Jsjnk4bw3YJqYzbdyBiNsPWHPfO++UGG749Cxs6peCu5Xg4nrena6OVxOYxrQTqww0Jmwt+Ref8rggumkTLz9Q=="],

    "ms": ["ms@2.1.3", "", {}, "sha512-6FlzubTLZG3J2a/NVCAleEhjzq5oxgHyaCU9yYXvcLsvoVaHJq/s5xXI6/XXP6tz7R9xAOtHnSO/tXtF3WRTlA=="],

    "nanoid": ["nanoid@3.3.20", "", { "bin": { "nanoid": "bin/nanoid.cjs" } }, "sha512-uKdg2G3GNCKQn9byYOpxbGqrT2fGO5KRt5J/8b3pok8rT6qxGWF6hxMyJiEYtAf+FVyYuD9hRaDqX5uPFYJ4ZQ=="],

    "neo-async": ["neo-async@2.6.2", "", {}, "sha512-Yd3UES5mWCSqR+qNT93S3UoYUkqAZ9lLg8a7g9rimsWmYGK8cVToA4/sF3RrshdyV3sAGMXVUmpMYOw+dLpOuw=="],

    "no-case": ["no-case@3.0.4", "", { "dependencies": { "lower-case": "^2.0.2", "tslib": "^2.0.3" } }, "sha512-fgAN3jGAh+RoxUGZHTSOLJIqUc2wmoBwGR4tbpNAKmmovFoWq0OdRkb0VkldReO2a2iBT/OEulG9XSUc10r3zg=="],

    "node-releases": ["node-releases@2.0.59", "", {}, "sha512-5qr2okC4ItAI0hG5SaV0HoYMpnM/Y6+Oqr7AmPYy/2uEoGvS+GbSKLeRxSS1uAdu59yz0ouzcuXievSgg///WA=="],

    "npm-run-path": ["npm-run-path@4.0.1", "", { "dependencies": { "path-key": "^3.0.0" } }, "sha512-S48WzZW777zhNIrn7gxOlISNAqi9ZC/uQFnRdbeIHhZhCA6UqpkOT8T1G7BvfdgP4Er8gF4sUbaS0i7QvIfCWw=="],

    "onetime": ["onetime@5.1.2", "", { "dependencies": { "mimic-fn": "^2.1.0" } }, "sha512-kbpaSSGJTWdAY5KPVeMOKXSrPtr8C8C7wodJbcsd51jRnmD+GZu8Y0VoU6Dm5Z4vWr0Ig/1NKuWRKf7j5aaYSg=="],

    "open": ["open@8.4.2", "", { "dependencies": { "define-lazy-prop": "^2.0.0", "is-docker": "^2.1.1", "is-wsl": "^2.2.0" } }, "sha512-7x81NCL719oNbsq/3mh+hVrAWmFuEYUqrq/Iw3kUzH8ReypT9QQ0BLoJS7/G9k6N81XjW4qHWtjWwe/9eLy1EQ=="],

    "parent-module": ["parent-module@1.0.1", "", { "dependencies": { "callsites": "^3.0.0" } }, "sha512-GQ2EWRpQV8/o+Aw8YqtfZZPfNRWZYkbidE9k5rpl/hC3vtHHBfGm2Ifi6qWV+coDGkrUKZAxE3Lot5kcsRlh+g=="],

    "parse-json": ["parse-json@5.2.0", "", { "dependencies": { "@babel/code-frame": "^7.0.0", "error-ex": "^1.3.1", "json-parse-even-better-errors": "^2.3.0", "lines-and-columns": "^1.1.6" } }, "sha512-ayCKvm/phCGxOkYRSCM82iDwct8/EonSEgCSxWxD7ve6jHggsFl4fZVQBPRNgQoKiuV/odhFrGzQXZwbifC8Rg=="],

    "path-key": ["path-key@3.1.1", "", {}, "sha512-ojmeN0qd+y0jszEtoY48r0Peq5dwMEkIlCOu6Q5f41lfkswXuKtYrhgoTpLnyIcHm24Uhqx+5Tqm2InSwLhE6Q=="],

    "path-type": ["path-type@4.0.0", "", {}, "sha512-gDKb8aZMDeD/tZWs9P6+q0J9Mwkdl6xMV8TjnGP3qJVJ06bdMgkbBlLU8IdfOsIsFz2BW1rNVT3XuNEl8zPAvw=="],

    "picocolors": ["picocolors@1.1.1", "", {}, "sha512-xceH2snhtb5M9liqDsmEw56le376mTZkEX/jEb/RxNFyegNul7eNslCXP9FDj/Lcu0X8KEyMceP2ntpaHrDEVA=="],

    "postcss": ["postcss@8.5.30", "", { "dependencies": { "nanoid": "^3.3.20", "picocolors": "^1.1.1", "source-map-js": "^1.2.2" } }, "sha512-zkd+e9S1AQHhmaBKye9zlFHWjOwVgqXl1q3ECYy8561K7qxR2cREf/STLskulBFd78k6AOFeA+ff1TtEzk9bAA=="],

    "postcss-modules-extract-imports": ["postcss-modules-extract-imports@3.1.0", "", { "peerDependencies": { "postcss": "^8.1.0" } }, "sha512-k3kNe0aNFQDAZGbin48pL2VNidTF0w4/eASDsxlyspobzU3wZQLOGj7L9gfRe0Jo9/4uud09DsjFNH7winGv8Q=="],

    "postcss-modules-local-by-default": ["postcss-modules-local-by-default@4.2.0", "", { "dependencies": { "icss-utils": "^5.0.0", "postcss-selector-parser": "^7.0.0", "postcss-value-parser": "^4.1.0" }, "peerDependencies": { "postcss": "^8.1.0" } }, "sha512-5kcJm/zk+GJDSfw+V/42fJ5fhjL5YbFDl8nVdXkJPLLW+Vf9mTD5Xe0wqIaDnLuL2U6cDNpTr+UQ+v2HWIBhzw=="],

    "postcss-modules-scope": ["postcss-modules-scope@3.2.1", "", { "dependencies": { "postcss-selector-parser": "^7.0.0" }, "peerDependencies": { "postcss": "^8.1.0" } }, "sha512-m9jZstCVaqGjTAuny8MdgE88scJnCiQSlSrOWcTQgM2t32UBe+MUmFSO5t7VMSfAf/FJKImAxBav8ooCHJXCJA=="],

    "postcss-modules-values": ["postcss-modules-values@4.0.0", "", { "dependencies": { "icss-utils": "^5.0.0" }, "peerDependencies": { "postcss": "^8.1.0" } }, "sha512-RDxHkAiEGI78gS2ofyvCsu7iycRv7oqw5xMWn9iMoR0N/7mf9D50ecQqUo5BZ9Zh2vH4bCUR/ktCqbB9m8vJjQ=="],

    "postcss-selector-parser": ["postcss-selector-parser@7.1.6", "", { "dependencies": { "cssesc": "^3.0.0", "util-deprecate": "^1.0.2" } }, "sha512-7qASPzhKF2l2KLboRZux8CCTRMdGiV08vWmyKzPz22qZ7ZjQBOeY7rNzNoCLSUiftJ7HUq0GERHmxw/t0dCdMw=="],

    "postcss-value-parser": ["postcss-value-parser@4.2.0", "", {}, "sha512-1NNCs6uurfkVbeXG4S8JFT9t19m45ICnif8zWLd5oPSZ50QnwMfK+H3jv408d4jw/7Bttv5axS5IiHoLaVNHeQ=="],

    "prismjs": ["prismjs@1.30.0", "", {}, "sha512-DEvV2ZF2r2/63V+tK8hQvrR2ZGn10srHbXviTlcv7Kpzw8jWiNTqbVgjO3IY8RxrrOUF8VPMQQFysYYYv0YZxw=="],

    "prompts": ["prompts@2.4.2", "", { "dependencies": { "kleur": "^3.0.3", "sisteransi": "^1.0.5" } }, "sha512-NxNv/kLguCA7p3jE8oL2aEBsrJWgAakBpgmgK6lpPWV+WuOmY6r2/zbAVnP+T8bQlA0nzHXSJSJW0Hq7ylaD2Q=="],

    "react": ["react@18.3.1", "", { "dependencies": { "loose-envify": "^1.1.0" } }, "sha512-wS+hAgJShR0KhEvPJArfuPVN1+Hz1t0Y6n5jLrGQbkb4urgPE/0Rve+1kMB1v/oWgHgm4WIcV+i7F2pTVj+2iQ=="],

    "react-dom": ["react-dom@18.3.1", "", { "dependencies": { "loose-envify": "^1.1.0", "scheduler": "^0.23.2" }, "peerDependencies": { "react": "^18.3.1" } }, "sha512-5m4nQKp+rZRb09LNH59GM4BxTh9251/ylbKIbpe7TpGxfJ+9kv6BLkLBXIjjspbgbnIBNqlI23tRnTWT0snUIw=="],

    "react-refresh": ["react-refresh@0.18.0", "", {}, "sha512-QgT5//D3jfjJb6Gsjxv0Slpj23ip+HtOpnNgnb2S5zU3CB26G/IDPGoy4RJB42wzFE46DRsstbW6tKHoKbhAxw=="],

    "recast": ["recast@0.23.21", "", { "dependencies": { "ast-types": "^0.16.1", "esprima": "~4.0.0", "source-map": "~0.6.1", "tiny-invariant": "^1.3.3", "tslib": "^2.0.1" } }, "sha512-mFAyJq9vUbSTARLZUvAEf1z3YxlvAwswbmxMx2mPA/MSm4KmpwvwvhsH/NIrZhyOuwD60Lzyw2qh83uCbgTPYw=="],

    "remotion": ["remotion@4.0.530", "", { "peerDependencies": { "react": ">=16.8.0", "react-dom": ">=16.8.0" } }, "sha512-7pp7F6P1Jdh/xncBiUGzNt9Vt4AMiw8M4KDtpM5J5KMN8JftlVuC/aGyUISjbUcWxf37x+YMDiPprWLecwIqkw=="],

    "require-from-string": ["require-from-string@2.0.2", "", {}, "sha512-Xf0nWe6RseziFMu+Ap9biiUbmplq6S9/p+7w7YXP/JBHhrUDDUhwa+vANyubuqfZWTveU//DYVGsDG7RKL/vEw=="],

    "resolve-from": ["resolve-from@4.0.0", "", {}, "sha512-pb/MYmXstAkysRFx8piNI1tGFNQIFA3vkE3Gq4EuA1dF6gHp/+vgZqsCGJapvy8N3Q+4o7FwvquPJcnZ7RYy4g=="],

    "scheduler": ["scheduler@0.23.2", "", { "dependencies": { "loose-envify": "^1.1.0" } }, "sha512-UOShsPwz7NrMUqhR6t0hWjFduvOzbtv7toDH1/hIrfRNIDBnnBWd0CwJTGvTpngVlmwGCdP9/Zl/tVrDqcuYzQ=="],

    "schema-utils": ["schema-utils@4.5.0", "", { "dependencies": { "@types/json-schema": "^7.0.15", "ajv": "^8.20.0", "ajv-formats": "^3.0.1", "ajv-keywords": "^5.1.0" } }, "sha512-zJlMCZ0cAR5p/Y4oVpRoqioDMJcGxaXRrQ/4rP4WyR84vc5z/DolXdbvXeDpTwbtocDFr2rhPqHPErDCUtz2kA=="],

    "semver": ["semver@7.5.3", "", { "dependencies": { "lru-cache": "^6.0.0" }, "bin": { "semver": "bin/semver.js" } }, "sha512-QBlUtyVk/5EeHbi7X0fw6liDZc7BBmEaSYn01fMU1OUYbf6GPsbTtd8WmnqbI20SeycoHSeiybkE/q1Q+qlThQ=="],

    "shebang-command": ["shebang-command@2.0.0", "", { "dependencies": { "shebang-regex": "^3.0.0" } }, "sha512-kHxr2zZpYtdmrN1qDjrrX/Z1rR1kG8Dx+gkpK1G4eXmvXswmcE1hTWBWYUzlraYw1/yZp6YuDY77YtvbN0dmDA=="],

    "shebang-regex": ["shebang-regex@3.0.0", "", {}, "sha512-7++dFhtcx3353uBaq8DDR4NuxBetBzC7ZQOhmTQInHEd6bSrXdiEyzCvG07Z44UYdLShWUyXt5M/yhz8ekcb1A=="],

    "signal-exit": ["signal-exit@3.0.7", "", {}, "sha512-wnD2ZE+l+SPC/uoS0vXeE9L1+0wuaMqKlfz9AMUo38JsyLSBWSFcHR1Rri62LZc12vLr1gb3jl7iwQhgwpAbGQ=="],

    "sisteransi": ["sisteransi@1.0.5", "", {}, "sha512-bLGGlR1QxBcynn2d5YmDX4MGjlZvy2MRBDRNHLJ8VI6l6+9FUiyTFNJ0IveOSP0bcXgVDPRcfGqA0pjaqUpfVg=="],

    "snake-case": ["snake-case@3.0.4", "", { "dependencies": { "dot-case": "^3.0.4", "tslib": "^2.0.3" } }, "sha512-LAOh4z89bGQvl9pFfNF8V146i7o7/CqFPbqzYgP+yYzDIDeS9HaNFtXABamRW+AQzEVODcvE79ljJ+8a9YSdMg=="],

    "source-map": ["source-map@0.8.0", "", {}, "sha512-d8EqvL+k/SOXCreS/SUzg2ciyHqBBLcN/yuRjFsbvVhHTE2pgei7oAhmPM7kWFbkX6OSMQfUq4KbkF3au9lhYQ=="],

    "source-map-js": ["source-map-js@1.2.2", "", {}, "sha512-KGj/8Y43x35aZVDtt+J4mK1hoLGHULMYfSkODJNQjNDC3oW1PqPoxMwo0pLUsWM/UEGzON/NxeHywEfNXNP3Vw=="],

    "source-map-support": ["source-map-support@0.5.21", "", { "dependencies": { "buffer-from": "^1.0.0", "source-map": "^0.6.0" } }, "sha512-uBHU3L3czsIyYXKX88fdrGovxdSCoTGDRZ6SYXtSRxLZUzHg5P/66Ht6uoUlHu9EZod+inXhKo3qQgwXUT/y1w=="],

    "stackframe": ["stackframe@1.3.4", "", {}, "sha512-oeVtt7eWQS+Na6F//S4kJ2K2VbRlS9D43mAlMyVpVWovy9o+jfgH8O9agzANzaiLjclA0oYzUXEM4PurhSUChw=="],

    "strip-final-newline": ["strip-final-newline@2.0.0", "", {}, "sha512-BrpvfNAE3dcvq7ll3xVumzjKjZQ5tI1sEUIKr3Uoks0XUl45St3FlatVqef9prk4jRDzhW6WZg+3bk93y6pLjA=="],

    "style-loader": ["style-loader@4.0.0", "", { "peerDependencies": { "webpack": "^5.27.0" } }, "sha512-1V4WqhhZZgjVAVJyt7TdDPZoPBPNHbekX4fWnCJL1yQukhCeZhJySUL+gL9y6sNdN95uEOS83Y55SqHcP7MzLA=="],

    "supports-color": ["supports-color@8.1.1", "", { "dependencies": { "has-flag": "^4.0.0" } }, "sha512-MpUEN2OodtUzxvKQl72cUF7RQ5EiHsGvSsVG0ia9c5RbWGL2CI4C7EpPS8UTBIplnlzZiNuV56w+FuNxy3ty2Q=="],

    "svg-parser": ["svg-parser@2.1.0", "", {}, "sha512-bwLf38YmY+TDYHJw1Ex0Co8c4yeXuJAo8YnXGZrscxrvYoVVIvLeniEkV1Ks/54VteMnL4FtyN1+P+TZJdUPmQ=="],

    "tapable": ["tapable@2.3.3", "", {}, "sha512-uxc/zpqFg6x7C8vOE7lh6Lbda8eEL9zmVm/PLeTPBRhh1xCgdWaQ+J1CUieGpIfm2HdtsUpRv+HshiasBMcc6A=="],

    "terser": ["terser@5.51.2", "", { "dependencies": { "@jridgewell/source-map": "^0.3.3", "acorn": "^8.15.0", "commander": "^2.20.0", "source-map-support": "~0.5.20" }, "bin": { "terser": "bin/terser" } }, "sha512-bWnjSNscmuI+GJze6ZupnHP8G/cTcsJF+bXCeQknk2SHQsgbNJnLrqiH9jZ2W4STPVXH2mDKKRX3iwPhc9Cn/Q=="],

    "terser-webpack-plugin": ["terser-webpack-plugin@5.6.1", "", { "dependencies": { "@jridgewell/trace-mapping": "^0.3.25", "jest-worker": "^27.4.5", "schema-utils": "^4.3.0", "terser": "^5.31.1" }, "peerDependencies": { "@minify-html/node": "*", "@swc/core": "*", "@swc/css": "*", "@swc/html": "*", "clean-css": "*", "cssnano": "*", "csso": "*", "esbuild": "*", "html-minifier-terser": "*", "lightningcss": "*", "postcss": "*", "uglify-js": "*", "webpack": "^5.1.0" }, "optionalPeers": ["@minify-html/node", "@swc/core", "@swc/css", "@swc/html", "clean-css", "cssnano", "csso", "esbuild", "html-minifier-terser", "lightningcss", "postcss", "uglify-js"] }, "sha512-201R5j+sJpK8nFWwKVyNfZot8FaJbLZDq5evriVzbV1wDtSXDjRUDRfJzHpAaxFDMEhsZL1QkeqM61wgsS3KaQ=="],

    "tiny-invariant": ["tiny-invariant@1.3.3", "", {}, "sha512-+FbBPE1o9QAYvviau/qC5SE3caw21q3xkvWKBtja5vgqOWIHHJ3ioaq1VPfn/Szqctz2bU/oYeKd9/z5BL+PVg=="],

    "to-fast-properties": ["to-fast-properties@2.0.0", "", {}, "sha512-/OaKK0xYrs3DmxRYqL/yDc+FxFUVYhDlXMhRmv3z915w2HF1tnN1omB354j8VUGO/hbRzyD6Y3sA7v7GS/ceog=="],

    "tslib": ["tslib@2.8.1", "", {}, "sha512-oJFu94HQb+KVduSUQL7wnpmqnfmLsOA/nAh6b6EH0wCEoK0/mPeXU6c3wKDV83MkOuHPRHtSXKKU99IBazS/2w=="],

    "undici-types": ["undici-types@8.9.0", "", {}, "sha512-KTDyRTYX8sWmKXAikPHHSyc63CRPETMctyjKFupcC6OBLXT3xsN0e9aF7m+mIXutFWpUXuedtowG7iLOzp0kQg=="],

    "update-browserslist-db": ["update-browserslist-db@1.3.4", "", { "dependencies": { "escalade": "^3.2.0", "picocolors": "^1.1.1" }, "peerDependencies": { "browserslist": ">= 4.21.0" }, "bin": { "update-browserslist-db": "cli.js" } }, "sha512-t8wonIOdQyOjtPd2VktlBu6QjTVTks6v8bSi7kd0r2Vll8TK1JYDZtRRdbmCHOAMphkZgrzK+L+vXK4pyZ8t4A=="],

    "util-deprecate": ["util-deprecate@1.0.2", "", {}, "sha512-EPD5q1uXyFxJpCrLnCc1nHnq3gOa6DZBocAIiI2TaSCA7VCJ1UJDMagCzIkXNsUYfD1daK//LTEQ8xiIbrHtcw=="],

    "watchpack": ["watchpack@2.6.1", "", { "dependencies": { "graceful-fs": "^4.1.2" } }, "sha512-8mk/LnXpQAiM2xKZhTkxikwly5GhL2Z+DWiLTkMa/E1Nfv9zURhHgiFyWvM4BWqW+LjIgL2AIS7JntEUx6v3vQ=="],

    "webpack": ["webpack@5.105.0", "", { "dependencies": { "@types/eslint-scope": "^3.7.7", "@types/estree": "^1.0.8", "@types/json-schema": "^7.0.15", "@webassemblyjs/ast": "^1.14.1", "@webassemblyjs/wasm-edit": "^1.14.1", "@webassemblyjs/wasm-parser": "^1.14.1", "acorn": "^8.15.0", "acorn-import-phases": "^1.0.3", "browserslist": "^4.28.1", "chrome-trace-event": "^1.0.2", "enhanced-resolve": "^5.19.0", "es-module-lexer": "^2.0.0", "eslint-scope": "5.1.1", "events": "^3.2.0", "glob-to-regexp": "^0.4.1", "graceful-fs": "^4.2.11", "json-parse-even-better-errors": "^2.3.1", "loader-runner": "^4.3.1", "mime-types": "^2.1.27", "neo-async": "^2.6.2", "schema-utils": "^4.3.3", "tapable": "^2.3.0", "terser-webpack-plugin": "^5.3.16", "watchpack": "^2.5.1", "webpack-sources": "^3.3.3" }, "peerDependencies": { "webpack-cli": "*" }, "optionalPeers": ["webpack-cli"], "bin": { "webpack": "bin/webpack.js" } }, "sha512-gX/dMkRQc7QOMzgTe6KsYFM7DxeIONQSui1s0n/0xht36HvrgbxtM1xBlgx596NbpHuQU8P7QpKwrZYwUX48nw=="],

    "webpack-sources": ["webpack-sources@3.6.0", "", {}, "sha512-EIMmPVvNI0CYXyRPp34F2Qk7W37/BZVZIofS6LAUnrNjCVahS+hO4mxwFJDjQjODTGZDtVzLYoN2+1dYkhk9qA=="],

    "which": ["which@2.0.2", "", { "dependencies": { "isexe": "^2.0.0" }, "bin": { "node-which": "./bin/node-which" } }, "sha512-BLI3Tl1TW3Pvl70l3yq3Y64i+awpwXqsGBYWkkqMtnbXgrMD+yj7rhW0kuEDxzJaYXGjEW5ogapKNMEKNMjibA=="],

    "ws": ["ws@8.21.0", "", { "peerDependencies": { "bufferutil": "^4.0.1", "utf-8-validate": ">=5.0.2" }, "optionalPeers": ["bufferutil", "utf-8-validate"] }, "sha512-Vsp28b7DRcimFQvrqu2Wek3z1iYxDCWqHYB8Qsnk/S4RfaCQzPGPyBNuVjJV3cd6UiKtUtp6sNM77gWvzcCH+g=="],

    "yallist": ["yallist@4.0.0", "", {}, "sha512-3wdGidZyq5PB084XLES5TpOSRA3wjXAlIWMhum2kRcv/41Sn2emQ0dycQW4uZXLejwKvg6EsvbdlVL+FYEct7A=="],

    "zod": ["zod@4.5.4", "", {}, "sha512-sC95tT5iHHH9gtpj6A81kh+NEaRAUFN+qlUPDUbRfOMvNf5QCBqsb3WgvnpVtK5Y+4UfA6KqufotuTvMGiTlsA=="],

    "@babel/core/@babel/parser": ["@babel/parser@7.29.9", "", { "dependencies": { "@babel/types": "^7.29.8" }, "bin": "./bin/babel-parser.js" }, "sha512-CjXrNHTnvqBVqHgdBysY3vk2T8tpJHb5/RMeHJBTyVa9xgugCB0CJTx/3oO8RV2QRQP391RWpB7D6hLjm8V9uA=="],

    "@babel/core/@babel/types": ["@babel/types@7.29.8", "", { "dependencies": { "@babel/helper-string-parser": "^7.29.7", "@babel/helper-validator-identifier": "^7.29.7" } }, "sha512-Vj1jF3cPfxg7OAfoI7QnVKLoILlm2JF9pnVHrX8qx7AHMiYWT+NDAA7jChlNgRS4WTLc/fD1lXLmPixluj+3Gg=="],

    "@babel/core/semver": ["semver@6.3.1", "", { "bin": { "semver": "bin/semver.js" } }, "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA=="],

    "@babel/generator/@babel/parser": ["@babel/parser@7.29.9", "", { "dependencies": { "@babel/types": "^7.29.8" }, "bin": "./bin/babel-parser.js" }, "sha512-CjXrNHTnvqBVqHgdBysY3vk2T8tpJHb5/RMeHJBTyVa9xgugCB0CJTx/3oO8RV2QRQP391RWpB7D6hLjm8V9uA=="],

    "@babel/generator/@babel/types": ["@babel/types@7.29.8", "", { "dependencies": { "@babel/helper-string-parser": "^7.29.7", "@babel/helper-validator-identifier": "^7.29.7" } }, "sha512-Vj1jF3cPfxg7OAfoI7QnVKLoILlm2JF9pnVHrX8qx7AHMiYWT+NDAA7jChlNgRS4WTLc/fD1lXLmPixluj+3Gg=="],

    "@babel/helper-compilation-targets/lru-cache": ["lru-cache@5.1.1", "", { "dependencies": { "yallist": "^3.0.2" } }, "sha512-KpNARQA3Iwv+jTA0utUVVbrh+Jlrr1Fv0e56GGzAFOXN7dk/FviaDW8LHmK52DlcH4WP2n6gI8vN1aesBFgo9w=="],

    "@babel/helper-compilation-targets/semver": ["semver@6.3.1", "", { "bin": { "semver": "bin/semver.js" } }, "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA=="],

    "@babel/helper-module-imports/@babel/types": ["@babel/types@7.29.8", "", { "dependencies": { "@babel/helper-string-parser": "^7.29.7", "@babel/helper-validator-identifier": "^7.29.7" } }, "sha512-Vj1jF3cPfxg7OAfoI7QnVKLoILlm2JF9pnVHrX8qx7AHMiYWT+NDAA7jChlNgRS4WTLc/fD1lXLmPixluj+3Gg=="],

    "@babel/helpers/@babel/types": ["@babel/types@7.29.8", "", { "dependencies": { "@babel/helper-string-parser": "^7.29.7", "@babel/helper-validator-identifier": "^7.29.7" } }, "sha512-Vj1jF3cPfxg7OAfoI7QnVKLoILlm2JF9pnVHrX8qx7AHMiYWT+NDAA7jChlNgRS4WTLc/fD1lXLmPixluj+3Gg=="],

    "@babel/template/@babel/parser": ["@babel/parser@7.29.9", "", { "dependencies": { "@babel/types": "^7.29.8" }, "bin": "./bin/babel-parser.js" }, "sha512-CjXrNHTnvqBVqHgdBysY3vk2T8tpJHb5/RMeHJBTyVa9xgugCB0CJTx/3oO8RV2QRQP391RWpB7D6hLjm8V9uA=="],

    "@babel/template/@babel/types": ["@babel/types@7.29.8", "", { "dependencies": { "@babel/helper-string-parser": "^7.29.7", "@babel/helper-validator-identifier": "^7.29.7" } }, "sha512-Vj1jF3cPfxg7OAfoI7QnVKLoILlm2JF9pnVHrX8qx7AHMiYWT+NDAA7jChlNgRS4WTLc/fD1lXLmPixluj+3Gg=="],

    "@babel/traverse/@babel/parser": ["@babel/parser@7.29.9", "", { "dependencies": { "@babel/types": "^7.29.8" }, "bin": "./bin/babel-parser.js" }, "sha512-CjXrNHTnvqBVqHgdBysY3vk2T8tpJHb5/RMeHJBTyVa9xgugCB0CJTx/3oO8RV2QRQP391RWpB7D6hLjm8V9uA=="],

    "@babel/traverse/@babel/types": ["@babel/types@7.29.8", "", { "dependencies": { "@babel/helper-string-parser": "^7.29.7", "@babel/helper-validator-identifier": "^7.29.7" } }, "sha512-Vj1jF3cPfxg7OAfoI7QnVKLoILlm2JF9pnVHrX8qx7AHMiYWT+NDAA7jChlNgRS4WTLc/fD1lXLmPixluj+3Gg=="],

    "css-loader/semver": ["semver@7.8.5", "", { "bin": { "semver": "bin/semver.js" } }, "sha512-Y7/KDsb8LjooZpwaqGyulO6DQlksgCncchHGk+sZIY4SBvUocMBEFH5Ur1fI4dV+Jvl0w6cjvucaIi40puRioA=="],

    "esrecurse/estraverse": ["estraverse@5.3.0", "", {}, "sha512-MMdARuVEQziNTeJD8DgMqmhwR11BRQ/cBP+pLtYdSTnf3MIO8fFeiINEbX36ZdNlfU/7A9f3gUw49B3oQsvwBA=="],

    "recast/ast-types": ["ast-types@0.16.3", "", { "dependencies": { "tslib": "^2.0.1" } }, "sha512-FvWoWYfSCM6kRxCSH+MGLHIKKGRL6A6AW7Zek2O32REPQRdg131428uRTKMBYAeRd3XXAaHDS60Wpri7CdKDrA=="],

    "recast/source-map": ["source-map@0.6.1", "", {}, "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g=="],

    "source-map-support/source-map": ["source-map@0.6.1", "", {}, "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g=="],

    "@babel/helper-compilation-targets/lru-cache/yallist": ["yallist@3.1.1", "", {}, "sha512-a4UGQaWPH59mOXUYnAG2ewncQS4i4F43Tv3JoAM+s2VDAmS9NsK8GpDMLrCHPksFT7h3K6TOoUNn2pb7RoXx4g=="],
  }
}
~~~~

### `package.json`

~~~~json
{
  "name": "lantern-library-probe",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "studio": "remotion studio",
    "still": "remotion still",
    "render": "remotion render"
  },
  "dependencies": {
    "@fontsource/cormorant-garamond": "5.2.11",
    "@fontsource/nunito-sans": "5.2.7",
    "@remotion/cli": "4.0.530",
    "react": "18.3.1",
    "react-dom": "18.3.1",
    "remotion": "4.0.530"
  }
}
~~~~

### `remotion.config.ts`

~~~~ts
import {Config} from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(92);
Config.setConcurrency(2);
~~~~

### `src/Branding.tsx`

~~~~tsx
import React from 'react';
import {AbsoluteFill} from 'remotion';
import {FortWorld} from './FortPoint';
import {Finish, flicker} from './Probe';
import {P} from './palette';

// Channel branding for Lantern Library, drawn in the same manner as the stories.
// Avatar: a hand lantern on night blue, readable at 98 px in a circle.
// Banner: the Fort Point world at night; text inside YouTube's safe area.
// Banner is laid out on 1920x1080 and rendered at --scale=1.3333 to 2560x1440 (recommended size).

export const Avatar: React.FC<{bg?: boolean}> = ({bg = true}) => (
	<AbsoluteFill style={{backgroundColor: bg ? P.night : 'transparent'}}>
		<svg width={800} height={800} viewBox="0 0 800 800">
			<defs>
				<radialGradient id="aGlow">
					<stop offset="0" stopColor={P.amber} stopOpacity="0.55" />
					<stop offset="0.45" stopColor={P.amber} stopOpacity="0.14" />
					<stop offset="1" stopColor={P.amber} stopOpacity="0" />
				</radialGradient>
				<radialGradient id="aBg" cx="0.5" cy="0.45" r="0.6">
					<stop offset="0" stopColor="#1f2748" />
					<stop offset="1" stopColor={P.night} />
				</radialGradient>
				<linearGradient id="aFlame" x1="0" y1="1" x2="0" y2="0">
					<stop offset="0" stopColor={P.coal} />
					<stop offset="0.4" stopColor={P.amber} />
					<stop offset="1" stopColor="#ffe9b8" />
				</linearGradient>
			</defs>
			{bg ? <rect width={800} height={800} fill="url(#aBg)" /> : null}
			<circle cx={400} cy={430} r={300} fill="url(#aGlow)" />
			{/* bail handle and cap */}
			<path d="M 310 250 Q 400 120 490 250" fill="none" stroke={P.plaster} strokeWidth="16" strokeLinecap="round" />
			<path d="M 300 262 L 500 262 L 470 222 L 330 222 Z" fill={P.plaster} />
			<rect x={372} y={196} width={56} height={30} rx={6} fill={P.plaster} />
			{/* glass globe with the flame */}
			<path d="M 318 268 Q 290 400 318 548 L 482 548 Q 510 400 482 268 Z" fill="#f6dfb0" opacity="0.22" stroke={P.plaster} strokeWidth="10" />
			<path d="M 400 330 C 432 380 446 414 446 452 C 446 486 426 506 400 506 C 374 506 354 486 354 452 C 354 414 368 380 400 330 Z" fill="url(#aFlame)" />
			<path d="M 400 410 C 414 434 420 450 420 466 C 420 482 412 492 400 492 C 388 492 380 482 380 466 C 380 450 386 434 400 410 Z" fill="#fff6e0" opacity="0.85" />
			{[340, 400, 460].map((x) => <line key={x} x1={x} x2={x} y1={272} y2={544} stroke={P.plaster} strokeWidth="6" opacity={x === 400 ? 0 : 0.9} />)}
			{/* base */}
			<rect x={296} y={548} width={208} height={40} rx={8} fill={P.plaster} />
			<rect x={318} y={588} width={164} height={22} rx={6} fill={P.plaster} opacity="0.8" />
		</svg>
	</AbsoluteFill>
);

const BANNER_WORLD = {t: 0.9, lamp: 1, cut: 0, f: 720, cam: {s: 2.0, cx: 905, cy: 447}, kitchen: 1, smoke: 1};

export const Banner: React.FC<{layer?: 'all' | 'bg' | 'text'; check?: boolean}> = ({layer = 'all', check = false}) => {
	const k = flicker(720, 1);
	// safe area 1235x338 of 2048x1152, laid out here at 1920x1080
	const u = 1920 / 2048;
	const box = (w: number, h: number) => ({left: (1920 - w * u) / 2, top: (1080 - h * u) / 2, width: w * u, height: h * u});
	return (
		<AbsoluteFill style={{backgroundColor: layer === 'text' ? 'transparent' : P.night}}>
			{layer === 'text' ? null : (
				<>
					<FortWorld st={BANNER_WORLD} />
					<AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(8,10,22,0.7) 0%, rgba(8,10,22,0.45) 45%, rgba(8,10,22,0) 62%)'}} />
					<Finish />
				</>
			)}
			{layer === 'bg' ? null : (
				<div style={{position: 'absolute', ...box(1235, 338), display: 'flex', flexDirection: 'column', justifyContent: 'center', paddingLeft: 24}}>
					<div style={{color: P.plaster, fontFamily: 'Cormorant Garamond', fontWeight: 600, fontSize: 112, lineHeight: 1, textShadow: `0 2px 30px rgba(5,7,15,${0.7 * k})`}}>Lantern Library</div>
					<div style={{color: P.plaster, opacity: 0.82, marginTop: 18, fontFamily: 'Nunito Sans', fontWeight: 600, fontSize: 25, letterSpacing: 5}}>
						ONE QUIET NIGHT IN ANOTHER CENTURY
					</div>
				</div>
			)}
			{check ? (
				<>
					<div style={{position: 'absolute', ...box(1235, 338), border: '3px dashed #ff6b6b', boxSizing: 'border-box'}}>
						<div style={{position: 'absolute', bottom: -34, left: 0, color: '#ff6b6b', fontFamily: 'Nunito Sans', fontSize: 20, fontWeight: 600, whiteSpace: 'nowrap'}}>
							safe area for text and logos: 1235 × 338 at 2048 × 1152, 1544 × 423 at 2560 × 1440
						</div>
					</div>
					<div style={{position: 'absolute', left: 16, top: 12, color: '#ffffff', fontFamily: 'Nunito Sans', fontSize: 20, fontWeight: 600}}>whole image: shown on TV</div>
				</>
			) : null}
		</AbsoluteFill>
	);
};
~~~~

### `src/Chapter.tsx`

~~~~tsx
import React from 'react';
import {AbsoluteFill, Audio, Easing, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {FortWorld, GROUND, TW, type FortState} from './FortPoint';
import {CoatPeg, Journal, KitchenLamp, LanternRoom, LensMemory, OilShelf, RulePage} from './Inserts';
import {Finish, Flame, lerp} from './Probe';
import {P} from './palette';
import tl from './chapter1.json';

// Chapter 1 "Dusk": the whole chapter on one timeline. Scene and cue times come
// from chapter1.json (tools/timeline.py). Without a voice they are estimated;
// with a voice the same keys get real times and everything below follows.

export const FPS = 30;
export const CHAPTER_FRAMES = Math.round(tl.duration * FPS);

const S = tl.scenes;
const at = (n: number, k = 0) => S[n - 1].start + k * (S[n - 1].end - S[n - 1].start);
const cue = (text: string) => {
	const c = tl.cues.find((x) => x.text.includes(text));
	if (!c) throw new Error(`no cue with "${text}"`);
	return c.start;
};
const ease = Easing.inOut(Easing.cubic);
const track = (sec: number, keys: [number, number][], easing = ease) => {
	const k = [...keys].sort((a, b) => a[0] - b[0]);
	for (let i = 1; i < k.length; i++) if (k[i][0] <= k[i - 1][0]) k[i][0] = k[i - 1][0] + 0.01;
	return interpolate(sec, k.map((x) => x[0]), k.map((x) => x[1]), {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing});
};
const ramp = (sec: number, a: number, b: number) => track(sec, [[a, 0], [b, 1]]);

// ---------- world camera: [time, scale, cx, cy] ----------
type Key = [number, number, number, number];
const CAM: Key[] = [
	[0, 9, 861, 658],
	[4.5, 9, 861, 658],
	[24, 1.25, 1000, 600],
	[at(2), 1.3, 980, 600],
	[cue("There is the keeper's house"), 2.6, 920, 640],
	[cue('And joined to the house'), 2.3, 1080, 600],
	[cue('That narrow brick room'), 3.2, 1070, 660],
	[cue('A light has stood'), 2.5, 1145, 540],
	[cue('A little way off'), 1.9, 1380, 620],
	[cue('Inside it hangs the fog bell'), 3.1, 1580, 640],
	[cue('Tonight, we will imagine'), 3.1, 1600, 640],
	[cue('Near the station there is a large hotel'), 2.2, 380, 610],
	[at(3) - 6, 2.1, 400, 610],
	[at(3) + 4, 1.35, 720, 570],
	[at(3, 1) - 2, 1.55, 900, 590],
	[at(4) + 2, 3.2, 930, 655],
	[at(4, 1) - 4, 3.6, 900, 665],
	[at(5) + 1, 8, 914, 668],
	[at(8) - 1, 3.2, 960, 655],
	[at(8) + 2, 3.2, 960, 655],
	[cue('You walk through the narrow'), 3.2, 980, 655],
	[cue('At the foot of the tower'), 3.0, 1110, 640],
	[cue('As you climb, the sounds'), 3.0, 1145, 590],
	[at(9), 3.4, 1145, 500],
	[at(12) - 1, 1.6, 1080, 560],
	[at(12) + 1, 1.6, 1080, 560],
	[at(12, 1) - 2, 1.32, 1000, 590],
	[at(13), 3.0, 1145, 560],
	[cue('The government register for this year lists'), 3.0, 1110, 640],
	[cue('For a keeper alone'), 3.0, 1000, 660],
	[cue('Later this evening, you will open'), 3.4, 1060, 670],
	[cue('Tomorrow is Sunday'), 1.5, 1040, 600],
	[at(14), 1.4, 1020, 590],
	[at(14, 1), 1.1, 1000, 520],
];
const camAt = (sec: number) => ({
	s: Math.exp(track(sec, CAM.map((k) => [k[0], Math.log(k[1])]))),
	cx: track(sec, CAM.map((k) => [k[0], k[2]])),
	cy: track(sec, CAM.map((k) => [k[0], k[3]])),
});

// ---------- sky, lamp, cut-away ----------
const skyAt = (sec: number) =>
	track(sec, [[0, 0.1], [at(3), 0.27], [at(4), 0.33], [at(8), 0.44], [at(11), 0.5], [at(12), 0.6], [at(12, 1), 0.84], [at(14, 1), 0.92]], Easing.linear);
const LIT = () => cue('The wick takes the flame');
const flameAt = (sec: number) =>
	track(sec, [[LIT(), 0], [LIT() + 2, 0.28], [cue('And slowly, the lens begins'), 0.32], [at(12) - 1, 1]]);
const fillAt = (sec: number) =>
	track(sec, [[LIT(), 0], [LIT() + 3, 0.15], [cue('And slowly, the lens begins'), 0.25], [at(12), 1]], Easing.inOut(Easing.sin));
const cutAt = (sec: number) =>
	track(sec, [[at(4) - 1, 0], [at(4) + 3, 1], [at(5) + 1, 1], [at(5) + 2, 0], [at(8) - 2, 0], [at(8) + 1, 1],
		[at(9) - 3, 1], [at(9), 0], [at(13) - 1, 0], [at(13) + 3, 1], [cue('Tomorrow is Sunday') - 1, 1], [cue('Tomorrow is Sunday') + 3, 0]]);

// ---------- the keeper: kitchen -> workroom -> switchback stairs ----------
const LEVELS = [GROUND - 2, 630, 560, 492];
const PATH: [number, number][] = [[930, GROUND - 6], [TW.x0 + 12, GROUND - 6]];
for (let i = 0; i < 3; i++) {
	const left = i % 2 === 0;
	PATH.push([left ? TW.x0 + 12 : TW.x1 - 12, LEVELS[i]]);
	PATH.push([left ? TW.x1 - 22 : TW.x0 + 22, LEVELS[i + 1] + 4]);
}
PATH.push([(TW.x0 + TW.x1) / 2, LEVELS[3] - 6]);
const SEG = PATH.slice(1).map((p, i) => Math.hypot(p[0] - PATH[i][0], p[1] - PATH[i][1]));
const TOTAL = SEG.reduce((a, b) => a + b, 0);
const along = (u: number) => {
	let d = Math.max(0, Math.min(1, u)) * TOTAL;
	for (let i = 0; i < SEG.length; i++) {
		if (d <= SEG[i] || i === SEG.length - 1) {
			const k = Math.min(1, d / SEG[i]);
			const a = PATH[i];
			const b = PATH[i + 1];
			return {x: lerp(a[0], b[0], k), y: lerp(a[1], b[1], k), facing: b[0] >= a[0] ? 1 : -1};
		}
		d -= SEG[i];
	}
	return {x: PATH[0][0], y: PATH[0][1], facing: 1};
};
const keeperAt = (sec: number): FortState['keeper'] => {
	if (sec > at(8) - 2 && sec < at(9)) {
		const u = track(sec, [[cue('You walk through the narrow'), 0], [cue('At the foot of the tower'), 0.18], [at(9) - 4, 1]], Easing.inOut(Easing.sin));
		const p = along(u);
		return {x: p.x, y: p.y, hand: 0, facing: p.facing, carry: sec > cue('You take the lamp')};
	}
	if (sec > at(13) - 1 && sec < cue('Later this evening, you will open') + 2) {
		const u = track(sec, [[at(13) + 2, 1], [cue('For a keeper alone') + 4, 0.1]], Easing.inOut(Easing.sin));
		const p = along(u);
		return {x: p.x, y: p.y, hand: 0, facing: -p.facing};
	}
	return undefined;
};

// ---------- close views laid over the world ----------
type Insert = {a: number; b: number; keep?: boolean; draw: (sec: number, k: number) => React.ReactNode};
const INSERTS: Insert[] = [
	{a: cue('It says that lights must be lighted'), b: cue('That is why the afternoon') + 2, draw: (sec, k) => <RuleInsert sec={sec} k={k} />},
	{a: at(5), b: at(6), keep: true, draw: (sec, k) => <KitchenLamp t={skyAt(sec)} f={sec * FPS} k={k} />},
	{a: at(6), b: at(7), keep: true, draw: (sec, k) => <OilShelf t={skyAt(sec)} f={sec * FPS} k={k} />},
	{a: at(7), b: cue('This morning, you wore'), keep: true, draw: (sec, k) => <CoatPeg t={skyAt(sec)} f={sec * FPS} k={k} skin={1} />},
	{a: cue('This morning, you wore'), b: cue('The book warns that a skin'), keep: true, draw: (sec, k) => <LensMemory f={sec * FPS} k={k} />},
	{a: cue('The book warns that a skin'), b: at(8), draw: (sec, k) => <CoatPeg t={skyAt(sec)} f={sec * FPS} k={k} skin={1} />},
	{a: at(9), b: at(12) + 4, draw: (sec) => <LanternInsert sec={sec} />},
	{a: cue('Later this evening, you will open'), b: cue('Tomorrow is Sunday'), draw: (sec, k) => (
		<Journal t={skyAt(sec)} f={sec * FPS} k={k} write={ramp(sec, cue('Each day takes one line') - 1, cue('One line for a whole day') + 3)} />
	)},
];
const insertOpacity = (sec: number, x: Insert) => {
	const fadeIn = ramp(sec, x.a - 1.2, x.a + 1.2);
	const fadeOut = x.keep ? ramp(sec, x.b + 1.2, x.b + 1.3) : ramp(sec, x.b - 1.2, x.b + 1.2);
	return fadeIn * (1 - fadeOut);
};

const LanternInsert: React.FC<{sec: number}> = ({sec}) => {
	const cam = {
		s: track(sec, [[at(9), 1.25], [at(9) + 6, 1.0], [at(10), 1.05], [at(10) + 20, 1.7], [at(11) - 4, 1.7], [at(11) + 4, 1.15], [at(12), 1.05]]),
		cx: 960,
		cy: track(sec, [[at(10), 540], [at(10) + 20, 470], [at(11) - 4, 470], [at(11) + 4, 560]]),
	};
	const curtains = track(sec, [[cue('You fold them, one at a time') - 2, 0], [cue('There is another rule here') + 2, 1]], Easing.linear);
	const lampIn = ramp(sec, cue('So you set it down') - 1, cue('So you set it down') + 5);
	const match = track(sec, [[cue('You strike a match'), 0], [LIT() + 1.5, 1]], Easing.linear);
	// inside the lantern the dusk reads darker than outside: keeps these minutes from standing out brighter
	return <LanternRoom t={Math.min(1, skyAt(sec) + 0.2)} f={sec * FPS} curtains={curtains} lampIn={lampIn} flame={flameAt(sec)} fill={fillAt(sec)} match={match} cam={cam} />;
};

const RuleInsert: React.FC<{sec: number; k: number}> = ({k}) => (
	<>
		<RulePage k={k} />
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', paddingBottom: 110}}>
			<div style={{width: 960, transform: `scale(${1 + 0.04 * k})`, color: '#2b241c', fontFamily: 'Cormorant Garamond', fontWeight: 600, fontSize: 54, lineHeight: 1.25, textAlign: 'center'}}>
				Lights must be lighted punctually at sunset, and must be kept burning at full intensity until sunrise.
				<div style={{marginTop: 30, fontFamily: 'Nunito Sans', fontSize: 22, letterSpacing: 4, color: '#5d5240'}}>
					INSTRUCTIONS TO LIGHT-KEEPERS, 1881 · ¶ 34
				</div>
			</div>
		</AbsoluteFill>
	</>
);

// ---------- narration as subtitles (no voice yet) ----------
const Captions: React.FC<{sec: number}> = ({sec}) => {
	const cues = tl.cues;
	let i = cues.findIndex((c) => c.start > sec) - 1;
	if (i === -2) i = cues.length - 1;
	if (i < 0) return null;
	const c = cues[i];
	const next = cues[i + 1]?.start ?? c.end + 3;
	const hold = Math.min(c.end + 1.2, next);
	if (sec > hold) return null;
	const o = Math.min(ramp(sec, c.start - 0.05, c.start + 0.3), 1 - ramp(sec, hold - 0.3, hold));
	return (
		<AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 70}}>
			<div style={{maxWidth: 1360, textAlign: 'center', opacity: o, color: P.plaster, fontFamily: 'Nunito Sans', fontWeight: 600, fontSize: 38, lineHeight: 1.35,
				textShadow: '0 0 18px rgba(5,7,15,0.95), 0 2px 4px rgba(5,7,15,0.9)'}}>
				{c.text}
			</div>
		</AbsoluteFill>
	);
};

// audio: ambience on; voice: the ElevenLabs track on, ambience 6 dB down under it;
// captions: narration burned in (the silent cut). The voiced pilot ships subtitles as a file.
export const Chapter: React.FC<{audio?: boolean; voice?: boolean; captions?: boolean}> = ({audio = true, voice = false, captions = true}) => {
	const frame = useCurrentFrame();
	const sec = frame / FPS;
	const f = frame;
	const st: FortState = {t: skyAt(sec), lamp: sec < at(12) - 2 ? 0 : 1, cut: cutAt(sec), cam: camAt(sec), keeper: keeperAt(sec), f, kitchen: track(sec, [[0, 0.9], [24, 0.55]]), smoke: 1};
	const ins = INSERTS.map((x) => ({x, o: insertOpacity(sec, x)})).filter((x) => x.o > 0);
	const covered = ins.some((x) => x.o >= 1);
	const worldIn = ramp(sec, 2.2, 4.6);
	const ident = track(sec, [[0, 0], [0.5, 1], [3.0, 1], [4.4, 0]]);
	const identText = track(sec, [[0.4, 0], [1.0, 1], [2.4, 1], [3.0, 0]]);
	const title = track(sec, [[9, 0], [11, 1], [21, 1], [23, 0]]);
	const end = ramp(sec, tl.duration - 7, tl.duration - 1);
	return (
		<AbsoluteFill style={{backgroundColor: P.night}}>
			{covered ? null : (
				<AbsoluteFill style={{opacity: worldIn}}>
					<FortWorld st={st} />
				</AbsoluteFill>
			)}
			{ins.map(({x, o}, i) => (
				<AbsoluteFill key={i} style={{opacity: o}}>
					{x.draw(sec, Math.max(0, Math.min(1, (sec - x.a) / Math.max(1, x.b - x.a))))}
				</AbsoluteFill>
			))}
			{title > 0 ? (
				<AbsoluteFill style={{padding: '110px 0 0 140px', justifyContent: 'flex-start', opacity: title}}>
					<div style={{color: P.plaster, opacity: 0.75, fontFamily: 'Nunito Sans', fontWeight: 600, fontSize: 19, letterSpacing: 6}}>FORT POINT, MAINE · JANUARY 1892 · PART 1</div>
					<div style={{color: P.plaster, fontFamily: 'Cormorant Garamond', fontWeight: 600, fontSize: 80, lineHeight: 1.05, marginTop: 10, textShadow: '0 2px 24px rgba(10,12,24,0.6)'}}>
						A Winter Night in a Maine Lighthouse
					</div>
				</AbsoluteFill>
			) : null}
			<Finish />
			{/* sleep grade: the whole picture a little darker, less so as the night deepens */}
			<AbsoluteFill style={{backgroundColor: '#05070f', opacity: track(sec, [[0, 0.33], [150, 0.3 - (0.15 * 150) / tl.duration], [tl.duration, 0.15]], Easing.linear)}} />
			{/* the ident flame stays bright: it is the channel's mark */}
			{ident > 0 ? <Flame f={f} size={22 * st.cam.s * 1.7} opacity={ident} /> : null}
			{identText > 0 ? (
				<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
					<div style={{marginTop: 440, opacity: identText, color: P.plaster, fontFamily: 'Nunito Sans', fontWeight: 600, fontSize: 20, letterSpacing: 9}}>LANTERN LIBRARY</div>
				</AbsoluteFill>
			) : null}
			{captions ? <Captions sec={sec} /> : null}
			<AbsoluteFill style={{backgroundColor: '#05070f', opacity: end}} />
			{audio ? <Audio src={staticFile('chapter1-ambience.wav')} volume={voice ? 0.5 : 1} /> : null}
			{audio && voice ? <Audio src={staticFile('chapter1-voice.wav')} /> : null}
		</AbsoluteFill>
	);
};
~~~~

### `src/FortPoint.tsx`

~~~~tsx
import React from 'react';
import {AbsoluteFill, interpolateColors, random} from 'remotion';
import {Finish, flicker, H, Keeper, lerp, pts, W} from './Probe';
import {P} from './palette';

// Key frames of Fort Point Light Station for the chapter 1 storyboard.
// Layout from the 1887 National Register nomination and the 1893 Light List:
// square white brick tower, narrow brick workroom, 1.5-storey frame house,
// pyramidal bell tower to the east-north-east, no oil house yet (1897),
// no long dormer yet (1899). Interiors are not documented: kept plain.
// t: 0 late afternoon, 0.5 sunset, 1 night. lamp: 0 unlit .. 1 full.

type Cam = {s: number; cx: number; cy: number};
export type FortState = {t: number; lamp: number; cut: number; cam: Cam; keeper?: {x: number; y: number; hand: number; facing: number; carry?: boolean}; f: number;
	kitchen?: number; smoke?: number};

export const c3 = (t: number, a: string, b: string, c: string) => interpolateColors(t, [0, 0.5, 1], [a, b, c]);
export const HORIZON = 560;
export const GROUND = 700;
export const TW = {x0: 1100, x1: 1190, top: 480}; // tower front face

const FortSky: React.FC<{t: number; f: number}> = ({t, f}) => {
	const top = c3(t, '#56627f', '#2a3159', '#0c1023');
	const mid = c3(t, '#8a91a8', '#4a4a70', '#151a35');
	const low = c3(t, '#c7beb2', '#87717e', '#242845');
	const glow = c3(t, '#e6d8c2', '#b08f85', '#2f3150');
	const sunY = lerp(452, 572, Math.min(1, t / 0.5));
	const stars = new Array(170).fill(0).map((_, i) => {
		const a = Math.max(0, Math.min(1, (t - 0.55 - random(`fa${i}`) * 0.3) / 0.15));
		const tw = 0.75 + 0.25 * Math.sin(f / (14 + random(`ft${i}`) * 30) + i);
		return (
			<circle key={i} cx={random(`fx${i}`) * W} cy={Math.pow(random(`fy${i}`), 1.3) * H * 0.5} r={0.5 + random(`fr${i}`) * 1.3}
				fill="#e7e4ef" opacity={a * tw * (0.35 + 0.55 * random(`fo${i}`))} />
		);
	});
	return (
		<svg width={W} height={H} style={{position: 'absolute'}}>
			<defs>
				<linearGradient id="fsky" x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor={top} />
					<stop offset="0.3" stopColor={mid} />
					<stop offset="0.48" stopColor={low} />
					<stop offset="0.53" stopColor={glow} />
				</linearGradient>
				<radialGradient id="fsun">
					<stop offset="0" stopColor="#fbf3e2" stopOpacity="0.95" />
					<stop offset="0.12" stopColor="#f1e3c8" stopOpacity="0.6" />
					<stop offset="1" stopColor={glow} stopOpacity="0" />
				</radialGradient>
			</defs>
			<rect width={W} height={H} fill="url(#fsky)" />
			{t < 0.55 ? <circle cx={300} cy={sunY} r={260} fill="url(#fsun)" opacity={1 - t * 1.6} /> : null}
			{t < 0.5 ? <circle cx={300} cy={sunY} r={13} fill="#fbf3e2" opacity={0.9 - t} /> : null}
			{stars}
		</svg>
	);
};

const Bay: React.FC<{t: number; f: number; lamp: number; win: number}> = ({t, f, lamp, win}) => {
	const near = c3(t, '#a2a6b6', '#5c5a79', '#1a2038');
	const far = c3(t, '#6e7891', '#3a3d5c', '#0e1327');
	const crest = c3(t, '#d6d3d2', '#8f879a', '#3d4562');
	const shore = c3(t, '#7c8098', '#4a4666', '#151933');
	const lines = [];
	for (let i = 0; i < 30; i++) {
		const k = i / 30;
		const y = HORIZON + 4 + 230 * Math.pow(k, 1.6);
		for (let j = 0; j < 10; j++) {
			const x = -400 + random(`bx${i}-${j}`) * 2800 + Math.sin(f / 80 + i + j) * (3 + 10 * k);
			lines.push(<line key={`${i}-${j}`} x1={x} x2={x + 20 + 120 * k * random(`bl${i}-${j}`)} y1={y} y2={y} stroke={crest}
				strokeWidth={0.6 + 1.6 * k} strokeLinecap="round" opacity={(0.08 + 0.2 * random(`bo${i}-${j}`)) * (0.6 + 0.4 * Math.sin(f / 40 + i))} />);
		}
	}
	const refl = (x: number, a: number, w: number, key: string, color: string) =>
		a < 0.01 ? null : new Array(22).fill(0).map((_, i) => {
			const k = i / 22;
			const y = HORIZON + 6 + 220 * Math.pow(k, 1.4);
			const ww = w * (0.4 + 1.5 * k) * (0.5 + random(`${key}${i}`));
			return <line key={key + i} x1={x - ww / 2 + Math.sin(f / 9 + i) * 4} x2={x + ww / 2 + Math.sin(f / 9 + i) * 4} y1={y} y2={y}
				stroke={color} strokeWidth={1 + 1.5 * k} opacity={a * (0.3 + 0.5 * random(`${key}o${i}`))} />;
		});
	return (
		<g>
			<defs>
				<linearGradient id="bay" x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor={near} />
					<stop offset="1" stopColor={far} />
				</linearGradient>
			</defs>
			<rect x={-800} y={HORIZON} width={3600} height={400} fill="url(#bay)" />
			{/* far shore of the bay */}
			<path d={`M -800 ${HORIZON} L -200 ${HORIZON - 9} Q 100 ${HORIZON - 16} 400 ${HORIZON - 8} Q 650 ${HORIZON - 3} 800 ${HORIZON - 6} L 1000 ${HORIZON} Z`} fill={shore} />
			<path d={`M 1500 ${HORIZON} Q 1800 ${HORIZON - 12} 2200 ${HORIZON - 5} L 2800 ${HORIZON} Z`} fill={shore} opacity="0.8" />
			{lines}
			{refl(300, t < 0.5 ? 0.45 * (1 - t * 1.6) : 0, 40, 'sr', '#f3e6cf')}
			{refl(1145, lamp, 22, 'lr', P.amber)}
			{refl(870, win * 0.3, 8, 'wr', P.amber)}
		</g>
	);
};

const Spruce: React.FC<{x: number; y: number; h: number; c: string}> = ({x, y, h, c}) => {
	const tiers = 7;
	const d = [`M ${x} ${y - h}`];
	for (let i = 1; i <= tiers; i++) {
		const yy = y - h + (h * 0.92 * i) / tiers;
		const w = (h * 0.32 * i) / tiers;
		d.push(`L ${x + w} ${yy} L ${x + w * 0.45} ${yy - h * 0.03}`);
	}
	for (let i = tiers; i >= 1; i--) {
		const yy = y - h + (h * 0.92 * i) / tiers;
		const w = (h * 0.32 * i) / tiers;
		d.push(`L ${x - w * 0.45} ${yy - h * 0.03} L ${x - w} ${yy}`);
	}
	d.push('Z');
	return (
		<g>
			<rect x={x - h * 0.012} y={y - h * 0.1} width={h * 0.024} height={h * 0.1} fill={c} />
			<path d={d.join(' ')} fill={c} />
		</g>
	);
};

// bare winter tree: deterministic branching
const Bare: React.FC<{x: number; y: number; h: number; c: string; seed: string}> = ({x, y, h, c, seed}) => {
	const out: React.ReactNode[] = [];
	const branch = (x0: number, y0: number, ang: number, len: number, w: number, depth: number, id: string) => {
		const x1 = x0 + Math.cos(ang) * len;
		const y1 = y0 - Math.sin(ang) * len;
		out.push(<line key={id} x1={x0} y1={y0} x2={x1} y2={y1} stroke={c} strokeWidth={w} strokeLinecap="round" />);
		if (depth === 0) return;
		const n = 2 + (random(seed + id) > 0.6 ? 1 : 0);
		for (let i = 0; i < n; i++) {
			const da = (i - (n - 1) / 2) * 0.55 + (random(seed + id + i) - 0.5) * 0.4;
			branch(x1, y1, ang + da, len * (0.68 + 0.12 * random(seed + id + 'l' + i)), w * 0.62, depth - 1, id + i);
		}
	};
	branch(x, y, Math.PI / 2, h * 0.34, h * 0.035, 6, 'r');
	return <g>{out}</g>;
};

const Hotel: React.FC<{t: number}> = ({t}) => {
	const wall = c3(t, '#9d9a96', '#5c5a70', '#1b1f33');
	const roof = c3(t, '#4a4e5f', '#2e3146', '#0f1222');
	const glass = c3(t, '#5f6780', '#3a3c58', '#121628');
	const x0 = 150;
	const x1 = 560;
	const wins = [];
	for (let r = 0; r < 3; r++) {
		for (let i = 0; i < 13; i++) {
			wins.push(<rect key={`${r}-${i}`} x={x0 + 18 + i * 30} y={585 + r * 30} width={10} height={16} fill={glass} />);
		}
	}
	return (
		<g>
			<rect x={x0} y={575} width={x1 - x0} height={GROUND - 575} fill={wall} />
			<polygon points={pts([[x0 - 8, 577], [x0 + 20, 548], [x1 - 20, 548], [x1 + 8, 577]])} fill={roof} />
			<rect x={330} y={520} width={46} height={58} fill={wall} />
			<polygon points={pts([[324, 522], [353, 498], [382, 522]])} fill={roof} />
			{wins}
			{/* long porch */}
			<rect x={x0 - 6} y={668} width={x1 - x0 + 12} height={4} fill={roof} />
			{new Array(15).fill(0).map((_, i) => <rect key={i} x={x0 + i * 29} y={671} width={2.5} height={29} fill={roof} />)}
		</g>
	);
};

const Station: React.FC<{st: FortState}> = ({st}) => {
	const {t, lamp, f} = st;
	const white = c3(t, '#e2dccf', '#9d97a2', '#3e4258');
	const whiteSide = c3(t, '#b5b2b2', '#6e6b82', '#262a40');
	const roof = c3(t, '#4b4f5f', '#2c3045', '#0e1121');
	const brick = c3(t, '#8a5d50', '#5a3c42', '#22171f');
	const iron = c3(t, '#262b3a', '#171b2a', '#090c17');
	const glass = c3(t, '#7a8199', '#454865', '#161a30');
	const darkWin = c3(t, '#3d4459', '#242840', '#0b0e1b');
	const win = Math.max(st.kitchen ?? 0, Math.min(1, Math.max(0, (t - 0.25) / 0.2)));
	const L = lamp * flicker(f, 1);
	const prism = interpolateColors(L, [0, 1], [c3(t, '#a5adbd', '#6a7090', '#33384f'), '#fff0cc']);
	const window = (x: number, y: number, w: number, h: number, lit: number, key: string) => (
		<g key={key}>
			{lit > 0 ? <circle cx={x + w / 2} cy={y + h / 2} r={30} fill="url(#fwGlow)" opacity={lit} /> : null}
			<rect x={x} y={y} width={w} height={h} fill={lit > 0 ? interpolateColors(lit, [0, 1], [darkWin, P.amber]) : darkWin} />
			<path d={`M ${x + w / 2} ${y} V ${y + h} M ${x} ${y + h / 2} H ${x + w}`} stroke={whiteSide} strokeWidth="1.2" />
			<rect x={x - 1.5} y={y - 1.5} width={w + 3} height={h + 3} fill="none" stroke={whiteSide} strokeWidth="1.5" />
		</g>
	);
	const cx = (TW.x0 + TW.x1) / 2;
	const shadow = Math.max(0, 1 - Math.abs(t - 0.3) / 0.2);
	const grassFurrow = c3(t, '#5b5448', '#37323f', '#0f111d');
	const smoke = st.smoke ?? 0;
	return (
		<g>
			<defs>
				<radialGradient id="fSmoke">
					<stop offset="0" stopColor={c3(t, '#d9d6d6', '#8d8698', '#3a3f58')} stopOpacity="0.5" />
					<stop offset="1" stopColor={c3(t, '#d9d6d6', '#8d8698', '#3a3f58')} stopOpacity="0" />
				</radialGradient>
				<radialGradient id="fwGlow">
					<stop offset="0" stopColor={P.amber} stopOpacity="0.5" />
					<stop offset="1" stopColor={P.amber} stopOpacity="0" />
				</radialGradient>
				<radialGradient id="fHalo">
					<stop offset="0" stopColor="#ffe6b0" stopOpacity="0.75" />
					<stop offset="0.25" stopColor={P.amber} stopOpacity="0.28" />
					<stop offset="1" stopColor={P.amber} stopOpacity="0" />
				</radialGradient>
				<radialGradient id="fBand" cx="0.5" cy="0.5" r="0.5">
					<stop offset="0" stopColor="#ffeac0" stopOpacity="0.6" />
					<stop offset="0.12" stopColor={P.amber} stopOpacity="0.28" />
					<stop offset="1" stopColor={P.amber} stopOpacity="0" />
				</radialGradient>
				<radialGradient id="fCore">
					<stop offset="0" stopColor="#fffaf0" />
					<stop offset="0.35" stopColor="#ffe2a0" stopOpacity="0.9" />
					<stop offset="1" stopColor={P.amber} stopOpacity="0" />
				</radialGradient>
			</defs>
			{/* long shadows of a low sun from the west-south-west */}
			<polygon points={pts([[TW.x0, GROUND], [TW.x1 + 16, GROUND - 6], [TW.x1 + 16 + 420 * shadow, GROUND + 26 * shadow], [TW.x0 + 380 * shadow, GROUND + 34 * shadow]])} fill="#1a1d2c" opacity={0.28 * shadow} />
			<polygon points={pts([[820, GROUND], [1040, GROUND], [1040 + 300 * shadow, GROUND + 22 * shadow], [820 + 300 * shadow, GROUND + 22 * shadow]])} fill="#1a1d2c" opacity={0.2 * shadow} />
			{/* the garden plot, asleep under the cold: a low picket fence */}
			<path d="M 430 716 L 552 716 M 430 709 L 552 709" stroke={whiteSide} strokeWidth="1.2" opacity="0.7" />
			{new Array(13).fill(0).map((_, i) => <rect key={`g${i}`} x={430 + i * 10} y={704} width={1.6} height={14} fill={whiteSide} opacity="0.7" />)}
			{/* barn */}
			<rect x={570} y={640} width={160} height={GROUND - 640} fill={white} />
			<polygon points={pts([[560, 642], [650, 598], [740, 642]])} fill={roof} />
			<rect x={630} y={662} width={36} height={38} fill={darkWin} />
			{/* house: ell, main block, chimney, windows, door */}
			<rect x={760} y={640} width={62} height={GROUND - 640} fill={whiteSide} />
			<polygon points={pts([[754, 642], [790, 616], [826, 642]])} fill={roof} />
			<rect x={820} y={622} width={220} height={GROUND - 622} fill={white} />
			<polygon points={pts([[812, 624], [846, 582], [1014, 582], [1048, 624]])} fill={roof} />
			{new Array(11).fill(0).map((_, i) => <line key={i} x1={820} x2={1040} y1={628 + i * 6.6} y2={628 + i * 6.6} stroke={whiteSide} strokeWidth="0.6" opacity="0.45" />)}
			{smoke > 0 ? new Array(14).fill(0).map((_, i) => {
				const life = ((f / 30 / 9 + i / 14) % 1);
				return <circle key={`sm${i}`} cx={992 + life * 70 + Math.sin(f / 50 + i) * 4} cy={556 - life * 120} r={5 + life * 26} fill="url(#fSmoke)" opacity={smoke * (1 - life) * Math.min(1, life * 6)} />;
			}) : null}
			<rect x={984} y={562} width={16} height={28} fill={brick} />
			<rect x={982} y={559} width={20} height={5} fill={roof} />
			{window(852, 645, 18, 26, win, 'k')}
			{window(892, 645, 18, 26, 0, 'w2')}
			{window(970, 645, 18, 26, 0, 'w3')}
			{window(777, 655, 14, 20, 0, 'w4')}
			<rect x={928} y={660} width={20} height={GROUND - 660} fill={roof} />
			<rect x={924} y={656} width={28} height={5} fill={whiteSide} />
			{/* narrow brick workroom */}
			<rect x={1040} y={652} width={TW.x0 - 1040} height={GROUND - 652} fill={brick} />
			{new Array(8).fill(0).map((_, i) => <line key={i} x1={1040} x2={TW.x0} y1={656 + i * 6} y2={656 + i * 6} stroke="#000" strokeWidth="0.5" opacity="0.2" />)}
			<polygon points={pts([[1036, 654], [1070, 640], [TW.x0, 654]])} fill={roof} />
			<rect x={1062} y={668} width={12} height={16} fill={darkWin} />
			{/* square tower: front face and a sliver of the east face */}
			<polygon points={pts([[TW.x1, TW.top], [TW.x1 + 16, TW.top - 6], [TW.x1 + 16, GROUND - 6], [TW.x1, GROUND]])} fill={whiteSide} />
			<rect x={TW.x0} y={TW.top} width={TW.x1 - TW.x0} height={GROUND - TW.top} fill={white} />
			{new Array(21).fill(0).map((_, i) => <line key={i} x1={TW.x0} x2={TW.x1} y1={TW.top + 8 + i * 10.4} y2={TW.top + 8 + i * 10.4} stroke={whiteSide} strokeWidth="0.5" opacity="0.25" />)}
			{window(cx - 7, 520, 14, 22, 0, 't1')}
			{window(cx - 7, 610, 14, 22, 0, 't2')}
			{/* deck, railing, lantern */}
			<polygon points={pts([[TW.x0 - 10, TW.top], [TW.x1 + 26, TW.top - 6], [TW.x1 + 26, TW.top - 13], [TW.x0 - 10, TW.top - 8]])} fill={iron} />
			<rect x={cx - 26} y={452} width={52} height={20} fill={iron} />
			<rect x={cx - 24} y={420} width={48} height={32} fill={glass} />
			<rect x={cx - 24} y={420} width={48} height={32} fill={P.amber} opacity={0.5 * L} />
			{/* lens: fourth order, small */}
			{new Array(13).fill(0).map((_, i) => {
				const y = 425.5 + i * 1.75;
				const k = Math.abs(i - 6) / 6;
				const w = 8.5 * Math.sqrt(1 - 0.55 * k * k);
				const belt = i >= 5 && i <= 7;
				return <line key={i} x1={cx - w} x2={cx + w} y1={y} y2={y} stroke={prism} strokeWidth={belt ? 1.6 : 1.1} opacity={(belt ? 0.75 : 0.5) + 0.25 * L} />;
			})}
			{[-6, 0, 6].map((d, i) => <line key={`rib${i}`} x1={cx + d} x2={cx + d} y1={425} y2={448} stroke="#7a6640" strokeWidth="0.45" opacity="0.8" />)}
			<rect x={cx - 9} y={448} width={18} height={3} fill="#5a4a32" />
			<circle cx={cx} cy={437} r={11 * L + 0.01} fill="url(#fCore)" />
			{[-24, -12, 0, 12, 24].map((d, i) => <line key={i} x1={cx + d} x2={cx + d} y1={420} y2={452} stroke={iron} strokeWidth={i === 0 || i === 4 ? 2 : 1.1} />)}
			<path d={`M ${cx - 28} 421 Q ${cx} 398 ${cx + 28} 421 Z`} fill={iron} />
			<circle cx={cx} cy={407} r={4} fill={iron} />
			<line x1={cx} x2={cx} y1={403} y2={392} stroke={iron} strokeWidth="0.9" />
			<line x1={cx + 32} x2={cx + 32} y1={474} y2={400} stroke={iron} strokeWidth="0.8" />
			<path d={`M ${TW.x0 - 8} 458 Q ${cx} 452 ${TW.x1 + 24} 458`} stroke={iron} strokeWidth="1.4" fill="none" />
			{new Array(12).fill(0).map((_, i) => <line key={i} x1={TW.x0 - 6 + i * 10.5} x2={TW.x0 - 6 + i * 10.5} y1={457} y2={470} stroke={iron} strokeWidth="0.8" />)}
			{/* light outside */}
			<ellipse cx={cx} cy={437} rx={1300} ry={13} fill="url(#fBand)" opacity={0.5 * L} style={{mixBlendMode: 'screen'}} />
			<circle cx={cx} cy={437} r={90} fill="url(#fHalo)" opacity={0.85 * L} style={{mixBlendMode: 'screen'}} />
			{/* bell tower, about 250 ft to the east-north-east: drawn smaller, further back */}
			<g transform="translate(1600 0)">
				<polygon points={pts([[-34, 696], [34, 696], [9, 600], [-9, 600]])} fill={white} />
				<polygon points={pts([[34, 696], [44, 692], [12, 598], [9, 600]])} fill={whiteSide} />
				<rect x={-10} y={592} width={20} height={9} fill={roof} />
				<rect x={-6} y={616} width={12} height={14} fill={darkWin} />
				<path d="M -4 618 Q 0 613 4 618 L 4.5 626 L -4.5 626 Z" fill={iron} />
			</g>
		</g>
	);
};

// interior in section: kitchen, workroom, tower stairs
const Section: React.FC<{st: FortState}> = ({st}) => {
	const {t, f, keeper} = st;
	const plaster = c3(t, '#7b6f66', '#4d4550', '#22202b');
	const dark = '#15131b';
	const floors = '#2a2430';
	const ember = 0.75 + 0.25 * Math.sin(f / 7) * Math.sin(f / 3.1);
	const hand = keeper?.hand ?? 0;
	const flights = [];
	// switchback stairs in the square tower
	const levels = [GROUND - 2, 630, 560, 492];
	for (let i = 0; i < 3; i++) {
		const y0 = levels[i];
		const y1 = levels[i + 1];
		const left = i % 2 === 0;
		const xa = left ? TW.x0 + 12 : TW.x1 - 12;
		const xb = left ? TW.x1 - 22 : TW.x0 + 22;
		flights.push(<line key={`s${i}`} x1={xa} y1={y0} x2={xb} y2={y1 + 4} stroke="#2e2934" strokeWidth="3.5" />);
		for (let k = 0; k < 9; k++) {
			const x = lerp(xa, xb, k / 9);
			const y = lerp(y0, y1 + 4, k / 9);
			flights.push(<line key={`t${i}-${k}`} x1={x - 3} x2={x + 3} y1={y - 3} y2={y - 3} stroke="#7d6b58" strokeWidth="1" opacity="0.6" />);
		}
		flights.push(<rect key={`l${i}`} x={TW.x0 + 8} y={y1 + 4} width={TW.x1 - TW.x0 - 16} height={3} fill={floors} />);
	}
	return (
		<g>
			<defs>
				<pattern id="fHatch" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
					<rect width="4" height="4" fill="#4a3a3a" />
					<line x1="0" y1="0" x2="0" y2="4" stroke="#2a2026" strokeWidth="1.4" />
				</pattern>
				<radialGradient id="fStove">
					<stop offset="0" stopColor={P.coal} stopOpacity="0.55" />
					<stop offset="1" stopColor={P.coal} stopOpacity="0" />
				</radialGradient>
				<radialGradient id="fHand">
					<stop offset="0" stopColor="#f6d39a" stopOpacity="0.8" />
					<stop offset="0.35" stopColor={P.amber} stopOpacity="0.3" />
					<stop offset="1" stopColor={P.amber} stopOpacity="0" />
				</radialGradient>
			</defs>
			{/* kitchen: back wall, floor, stove, table with the filled lamp, chair */}
			<rect x={824} y={626} width={212} height={GROUND - 626} fill={plaster} />
			<rect x={824} y={GROUND - 6} width={212} height={6} fill={floors} />
			<rect x={824} y={622} width={212} height={4} fill={dark} />
			<rect x={858} y={640} width={20} height={26} fill={c3(t, '#8d93a6', '#4c4d6a', '#151a30')} />
			<path d="M 868 640 V 666 M 858 653 H 878" stroke={dark} strokeWidth="1.2" />
			<rect x={985} y={664} width={34} height={30} fill={dark} />
			<rect x={987} y={694} width={4} height={6} fill={dark} />
			<rect x={1013} y={694} width={4} height={6} fill={dark} />
			<rect x={998} y={626} width={6} height={38} fill={dark} />
			<rect x={991} y={678} width={22} height={6} fill={P.coal} opacity={0.6 * ember} />
			<circle cx={1002} cy={682} r={40} fill="url(#fStove)" opacity={ember} />
			<rect x={890} y={672} width={52} height={3} fill="#3a2e2a" />
			<rect x={893} y={675} width={3} height={25} fill="#3a2e2a" />
			<rect x={936} y={675} width={3} height={25} fill="#3a2e2a" />
			{keeper?.carry || st.lamp > 0 ? null : (
				<g>
					<rect x={910} y={660} width={9} height={12} rx={2} fill="#9c8048" />
					<rect x={912} y={652} width={5} height={8} rx={2} fill="#c9c3b6" opacity="0.7" />
				</g>
			)}
			<rect x={850} y={684} width={30} height={12} rx={1.5} fill="#3b3028" />
			<rect x={850} y={684} width={30} height={3} fill="#4d3d30" />
			<rect x={863} y={688} width={4} height={3} fill="#8a7448" />
			<rect x={955} y={674} width={3} height={26} fill="#3a2e2a" />
			<rect x={955} y={674} width={14} height={3} fill="#3a2e2a" />
			{/* workroom: shelf with closed oil cans, coat and cap on a peg, folded apron */}
			<rect x={1044} y={656} width={TW.x0 - 1044} height={GROUND - 656} fill={plaster} />
			<rect x={1046} y={668} width={50} height={2} fill={dark} />
			{[0, 1, 2].map((i) => <rect key={i} x={1050 + i * 13} y={656} width={9} height={12} rx={1.5} fill="#7c7a72" />)}
			<path d="M 1082 676 L 1077 699 L 1093 699 L 1088 676 Z" fill="#1d2235" />
			<rect x={1080} y={672} width={10} height={4} fill="#1d2235" />
			<rect x={1050} y={688} width={14} height={4} fill="#d9d2c2" />
			{/* tower interior */}
			<rect x={TW.x0 + 7} y={TW.top + 6} width={TW.x1 - TW.x0 - 14} height={GROUND - TW.top - 6} fill={plaster} />
			{flights}
			<rect x={TW.x0 + 7} y={TW.top + 2} width={TW.x1 - TW.x0 - 14} height={6} fill={dark} />
			<rect x={(TW.x0 + TW.x1) / 2 - 8} y={TW.top + 2} width={16} height={6} fill="#4a3f38" />
			{/* wall section faces */}
			<rect x={TW.x0} y={TW.top} width={7} height={GROUND - TW.top} fill="url(#fHatch)" />
			<rect x={TW.x1 - 7} y={TW.top} width={7} height={GROUND - TW.top} fill="url(#fHatch)" />
			<rect x={1040} y={652} width={4} height={GROUND - 652} fill="url(#fHatch)" />
			<rect x={820} y={622} width={4} height={GROUND - 622} fill="#2a2430" />
			{keeper ? <circle cx={keeper.x + 6} cy={keeper.y - 11} r={60} fill="url(#fHand)" opacity={hand} style={{mixBlendMode: 'screen'}} /> : null}
		</g>
	);
};

const Ground: React.FC<{t: number}> = ({t}) => {
	const grass = c3(t, '#7d735f', '#4b4450', '#171a2a');
	const grassDark = c3(t, '#5b5448', '#37323f', '#0f111d');
	const rock = c3(t, '#5d5f6c', '#36384d', '#11141f');
	const blades = new Array(260).fill(0).map((_, i) => {
		const x = -300 + random(`gx${i}`) * 2500;
		const y = GROUND + 4 + Math.pow(random(`gy${i}`), 1.6) * 380;
		const h = 4 + 10 * ((y - GROUND) / 380) + random(`gh${i}`) * 5;
		return <path key={i} d={`M ${x} ${y} l ${-2 + random(`gl${i}`) * 4} ${-h}`} stroke={grassDark} strokeWidth={0.7 + 1.2 * ((y - GROUND) / 380)} opacity="0.8" />;
	});
	return (
		<g>
			{/* bluff above the water on the right */}
			<path d={`M 1500 ${GROUND - 4} Q 1720 ${GROUND - 6} 1840 ${GROUND + 20} L 1980 ${HORIZON + 120} L 2400 ${HORIZON + 140} L 2400 1200 L 1500 1200 Z`} fill={rock} />
			<path d={`M -400 ${GROUND + 6} Q 300 ${GROUND - 12} 900 ${GROUND - 2} Q 1400 ${GROUND + 4} 1840 ${GROUND + 14} Q 1900 ${GROUND + 60} 1960 1200 L -400 1200 Z`} fill={grass} />
			<path d={`M -400 900 Q 400 850 1000 930 Q 1500 990 2000 960 L 2000 1200 L -400 1200 Z`} fill={grassDark} opacity="0.55" />
			{new Array(14).fill(0).map((_, i) => (
				<ellipse key={`p${i}`} cx={-200 + random(`px${i}`) * 2300} cy={GROUND + 30 + random(`py${i}`) * 300} rx={120 + random(`pr${i}`) * 260} ry={4 + random(`pq${i}`) * 12}
					fill={grassDark} opacity={0.08 + 0.1 * random(`po${i}`)} />
			))}
			{blades}
		</g>
	);
};

export const FortWorld: React.FC<{st: FortState}> = ({st}) => {
	const {t, cam, keeper, cut, f, lamp} = st;
	const tree = c3(t, '#3b4048', '#252a3b', '#0b0e1b');
	const bare = c3(t, '#6a6466', '#3c3849', '#121526');
	const win = Math.max(0, Math.min(1, (t - 0.25) / 0.2));
	return (
		<>
			<FortSky t={t} f={f} />
			<svg width={W} height={H} style={{position: 'absolute'}}>
				<g transform={`translate(${W / 2} ${H / 2}) scale(${cam.s}) translate(${-cam.cx} ${-cam.cy})`}>
					<Bay t={t} f={f} lamp={lamp} win={win} />
					<Spruce x={90} y={GROUND} h={190} c={tree} />
					<Bare x={250} y={GROUND} h={200} c={bare} seed="a" />
					<Hotel t={t} />
					<Spruce x={120} y={GROUND + 6} h={150} c={tree} />
					<Spruce x={540} y={GROUND} h={170} c={tree} />
					<Bare x={1320} y={GROUND} h={180} c={bare} seed="b" />
					<Ground t={t} />
					<Station st={st} />
					{cut > 0 ? <g opacity={cut}><Section st={st} /></g> : null}
					{keeper ? <Keeper x={keeper.x} y={keeper.y} step={f / 3} hand={keeper.hand} f={f} facing={keeper.facing} /> : null}
					{keeper?.carry ? (
						<g transform={`translate(${keeper.x + 7 * keeper.facing} ${keeper.y - 12})`}>
							<rect x={-2.5} y={0} width={5} height={6} rx={1} fill="#9c8048" />
							<rect x={-1.4} y={-4} width={2.8} height={4} rx={1} fill="#c9c3b6" opacity="0.7" />
						</g>
					) : null}
					<Spruce x={1900} y={GROUND + 40} h={260} c={tree} />
					<Spruce x={-60} y={GROUND + 60} h={300} c={tree} />
				</g>
			</svg>
		</>
	);
};

const FRAMES: Record<string, FortState> = {
	// scene 2: the point in late afternoon
	K1: {t: 0.18, lamp: 0, cut: 0, f: 120, cam: {s: 1.5, cx: 1080, cy: 610}},
	// scene 8: through the workroom, the house and tower open in section; you carry the filled lamp
	K2: {t: 0.42, lamp: 0, cut: 1, f: 300, cam: {s: 2.75, cx: 1000, cy: 572}, keeper: {x: 1150, y: 597, hand: 0, facing: -1, carry: true}},
	// scene 11: the lamp lit, the flame still low
	K3: {t: 0.6, lamp: 0.45, cut: 0, f: 500, cam: {s: 6.5, cx: 1150, cy: 440}},
	// scene 12: light over the water, first stars, the hotel dark
	K4: {t: 0.85, lamp: 1, cut: 0, f: 700, cam: {s: 1.45, cx: 1060, cy: 600}},
};

export const FortFrame: React.FC<{frame: string}> = ({frame}) => (
	<AbsoluteFill style={{backgroundColor: P.night}}>
		<FortWorld st={FRAMES[frame]} />
		<Finish />
	</AbsoluteFill>
);
~~~~

### `src/Inserts.tsx`

~~~~tsx
import React from 'react';
import {interpolateColors, random} from 'remotion';
import {c3} from './FortPoint';
import {flicker, H, lerp, pts, W} from './Probe';
import {P} from './palette';

// Close views of the station for chapter 1, drawn in the same manner as the
// world. Interiors are not documented: plain, only what the narration needs.
// t: sky time as in FortWorld. k: 0..1 progress through the insert.

const drift = (k: number, x = 960, y = 540, amount = 0.05) =>
	`translate(${x} ${y}) scale(${1 + amount * k}) translate(${-x} ${-y})`;

const Sky: React.FC<{t: number; id: string; x: number; y: number; w: number; h: number; horizon: number}> = ({t, id, x, y, w, h, horizon}) => (
	<g>
		<defs>
			<linearGradient id={id} x1="0" y1="0" x2="0" y2="1">
				<stop offset="0" stopColor={c3(t, '#7a84a0', '#3a3f68', '#0e1228')} />
				<stop offset="0.75" stopColor={c3(t, '#c7beb2', '#87717e', '#242845')} />
				<stop offset="1" stopColor={c3(t, '#e6d8c2', '#b08f85', '#2f3150')} />
			</linearGradient>
		</defs>
		<rect x={x} y={y} width={w} height={horizon - y} fill={`url(#${id})`} />
		<rect x={x} y={horizon} width={w} height={y + h - horizon} fill={c3(t, '#8e93a6', '#4f4e6e', '#141a32')} />
		<path d={`M ${x} ${horizon} Q ${x + w * 0.4} ${horizon - 14} ${x + w} ${horizon - 4} L ${x + w} ${horizon} Z`} fill={c3(t, '#6e7891', '#3a3d5c', '#0e1327')} />
	</g>
);

const Sash: React.FC<{x: number; y: number; w: number; h: number; cols: number; rows: number; c: string}> = ({x, y, w, h, cols, rows, c}) => (
	<g>
		<rect x={x - 14} y={y - 14} width={w + 28} height={h + 28} fill="none" stroke={c} strokeWidth="28" />
		{new Array(cols - 1).fill(0).map((_, i) => <rect key={`c${i}`} x={x + ((i + 1) * w) / cols - 4} y={y} width={8} height={h} fill={c} />)}
		{new Array(rows - 1).fill(0).map((_, i) => <rect key={`r${i}`} x={x} y={y + ((i + 1) * h) / rows - 5} width={w} height={10} fill={c} />)}
	</g>
);

// ---------- scene 4: the filled lamp waits on the kitchen table ----------
export const KitchenLamp: React.FC<{t: number; f: number; k: number}> = ({t, f, k}) => {
	const wall = c3(t, '#7d7066', '#4f4650', '#211e29');
	const wood = c3(t, '#5e4636', '#3e2f2c', '#1a1519');
	const frame = c3(t, '#cfc8bb', '#8a8494', '#33364a');
	const ember = 0.75 + 0.25 * Math.sin(f / 7) * Math.sin(f / 3.1);
	const daylight = Math.max(0, 1 - t / 0.55);
	return (
		<svg width={W} height={H} style={{position: 'absolute'}}>
			<defs>
				<linearGradient id="kBrass" x1="0" y1="0" x2="1" y2="0">
					<stop offset="0" stopColor="#d9b56c" />
					<stop offset="0.3" stopColor="#a8814a" />
					<stop offset="1" stopColor="#4f3b25" />
				</linearGradient>
				<radialGradient id="kEmber">
					<stop offset="0" stopColor={P.coal} stopOpacity="0.55" />
					<stop offset="1" stopColor={P.coal} stopOpacity="0" />
				</radialGradient>
				<linearGradient id="kBeam" x1="0" y1="0" x2="1" y2="1">
					<stop offset="0" stopColor="#dfe3ee" stopOpacity="0.22" />
					<stop offset="1" stopColor="#dfe3ee" stopOpacity="0" />
				</linearGradient>
			</defs>
			<g transform={drift(k, 1000, 640)}>
				<rect width={W} height={H} fill={wall} />
				{new Array(9).fill(0).map((_, i) => <rect key={i} x={0} y={60 + i * 70} width={W} height={1} fill="#000" opacity="0.06" />)}
				<Sky t={t} id="kSky" x={180} y={140} w={430} h={480} horizon={470} />
				<Sash x={180} y={140} w={430} h={480} cols={2} rows={3} c={frame} />
				{/* window light falls across the table and wall */}
				<polygon points={pts([[610, 160], [610, 640], [1500, 980], [1250, 420]])} fill="url(#kBeam)" opacity={daylight} />
				{/* stove, its pipe and the ember glow */}
				<rect x={1560} y={0} width={44} height={560} fill="#17151b" />
				<rect x={1420} y={560} width={330} height={360} rx={8} fill="#1b1a20" />
				<rect x={1405} y={548} width={360} height={22} rx={4} fill="#252329" />
				<rect x={1470} y={760} width={230} height={50} rx={6} fill={P.coal} opacity={0.5 * ember} />
				{new Array(7).fill(0).map((_, i) => <rect key={i} x={1478 + i * 32} y={760} width={8} height={50} fill="#1b1a20" />)}
				<circle cx={1585} cy={790} r={360} fill="url(#kEmber)" opacity={ember} />
				<path d="M 1500 548 Q 1500 480 1560 476 Q 1620 476 1620 548 Z" fill="#2a282e" />
				<path d="M 1620 510 L 1680 490" stroke="#2a282e" strokeWidth="12" strokeLinecap="round" />
				{/* table */}
				<polygon points={pts([[0, 760], [1400, 740], [1920, 1080], [0, 1080]])} fill={wood} />
				<polygon points={pts([[0, 760], [1400, 740], [1400, 756], [0, 778]])} fill="#000" opacity="0.18" />
				{/* the brass lamp: font, burner, glass chimney, unlit wick */}
				<ellipse cx={980} cy={880} rx={150} ry={22} fill="#000" opacity="0.25" />
				<path d="M 860 870 Q 860 760 900 730 L 1060 730 Q 1100 760 1100 870 Z" fill="url(#kBrass)" />
				<ellipse cx={980} cy={870} rx={120} ry={16} fill="#5c4529" />
				<rect x={930} y={700} width={100} height={34} rx={6} fill="url(#kBrass)" />
				<rect x={952} y={682} width={56} height={22} fill="#6d5330" />
				<path d="M 948 682 Q 930 600 950 540 Q 962 500 962 420 L 998 420 Q 998 500 1010 540 Q 1030 600 1012 682 Z"
					fill="#d8dde6" opacity="0.18" stroke="#e8ecf2" strokeOpacity="0.35" strokeWidth="2" />
				<path d="M 952 660 Q 940 600 956 548" stroke="#ffffff" strokeOpacity={0.25 + 0.3 * daylight} strokeWidth="4" fill="none" />
				<rect x={975} y={668} width={10} height={16} fill="#e8e0cc" />
				<path d="M 878 850 Q 880 780 910 750" stroke="#f5dca0" strokeOpacity={0.3 + 0.4 * daylight} strokeWidth="5" fill="none" />
			</g>
		</svg>
	);
};

// ---------- scene 5: closed oil cans on the workroom shelf ----------
export const OilShelf: React.FC<{t: number; f: number; k: number}> = ({t, k}) => {
	const brick = c3(t, '#7d5649', '#4e3439', '#1d1419');
	const mortar = c3(t, '#5a4038', '#36262b', '#120d11');
	const tin = c3(t, '#a7aab0', '#6d6f80', '#2b2d3c');
	const tinDark = c3(t, '#6c6f78', '#43455a', '#181a26');
	const plank = c3(t, '#5e4636', '#3e2f2c', '#1a1519');
	const frame = c3(t, '#cfc8bb', '#8a8494', '#33364a');
	const daylight = Math.max(0, 1 - t / 0.55);
	const bricks = [];
	for (let r = 0; r < 26; r++) {
		for (let i = 0; i < 18; i++) {
			const x = i * 120 - (r % 2) * 60;
			bricks.push(<rect key={`${r}-${i}`} x={x + 3} y={r * 42 + 3} width={114} height={36} fill={brick} opacity={0.85 + 0.15 * random(`ob${r}-${i}`)} />);
		}
	}
	const can = (x: number, y: number, s: number, key: string) => (
		<g key={key} transform={`translate(${x} ${y}) scale(${s})`}>
			<rect x={-70} y={-200} width={140} height={200} rx={6} fill={tin} />
			<rect x={-70} y={-200} width={40} height={200} fill="#fff" opacity="0.08" />
			<rect x={30} y={-200} width={40} height={200} fill="#000" opacity="0.18" />
			<polygon points={pts([[-70, -200], [-40, -240], [40, -240], [70, -200]])} fill={tinDark} />
			<rect x={-14} y={-262} width={28} height={24} rx={3} fill={tinDark} />
			<rect x={-18} y={-268} width={36} height={10} rx={3} fill="#2a2b33" />
			<rect x={-70} y={-140} width={140} height={6} fill={tinDark} />
			<rect x={-70} y={-60} width={140} height={6} fill={tinDark} />
		</g>
	);
	return (
		<svg width={W} height={H} style={{position: 'absolute'}}>
			<defs>
				<linearGradient id="oBeam" x1="1" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor="#dfe3ee" stopOpacity="0.25" />
					<stop offset="1" stopColor="#dfe3ee" stopOpacity="0" />
				</linearGradient>
			</defs>
			<g transform={drift(k, 800, 560)}>
				<rect width={W} height={H} fill={mortar} />
				{bricks}
				<Sky t={t} id="oSky" x={1440} y={180} w={300} h={330} horizon={420} />
				<Sash x={1440} y={180} w={300} h={330} cols={2} rows={2} c={frame} />
				<polygon points={pts([[1440, 200], [1440, 510], [500, 980], [700, 560]])} fill="url(#oBeam)" opacity={daylight} />
				{/* shelf */}
				<rect x={140} y={600} width={1180} height={26} fill={plank} />
				<rect x={140} y={626} width={1180} height={6} fill="#000" opacity="0.3" />
				<path d="M 220 626 L 220 700 L 290 626 Z M 1220 626 L 1220 700 L 1150 626 Z" fill={plank} />
				{can(330, 600, 1, 'c1')}
				{can(560, 600, 1, 'c2')}
				{can(790, 600, 1, 'c3')}
				{can(1020, 600, 0.8, 'c4')}
				{/* a funnel and a measure on nails */}
				<polygon points={pts([[1180, 300], [1290, 300], [1245, 380], [1225, 380]])} fill={tinDark} />
				<rect x={1229} y={380} width={12} height={60} fill={tinDark} />
				<circle cx={1235} cy={292} r={5} fill="#222" />
				{/* floor and a wooden box */}
				<rect x={0} y={960} width={W} height={120} fill={plank} />
				<rect x={260} y={840} width={360} height={130} fill={plank} />
				<rect x={260} y={840} width={360} height={10} fill="#000" opacity="0.25" />
			</g>
		</svg>
	);
};

// ---------- scene 6: coat, cap and folded apron by the workroom door ----------
export const CoatPeg: React.FC<{t: number; f: number; k: number; skin: number}> = ({t, k, skin}) => {
	const wall = c3(t, '#8a8076', '#57505a', '#24212c');
	const board = c3(t, '#7a7068', '#4b4450', '#1e1b25');
	const navy = c3(t, '#26304f', '#1a2140', '#0b0f1f');
	const navyLit = c3(t, '#38446a', '#252d52', '#111628');
	const wood = c3(t, '#5e4636', '#3e2f2c', '#1a1519');
	const linen = c3(t, '#ddd5c4', '#a39c9e', '#45475a');
	return (
		<svg width={W} height={H} style={{position: 'absolute'}}>
			<g transform={drift(k, 900, 520)}>
				<rect width={W} height={H} fill={wall} />
				{new Array(16).fill(0).map((_, i) => <rect key={i} x={i * 128} y={0} width={3} height={H} fill={board} />)}
				{/* door frame of the workroom on the right */}
				<rect x={1380} y={0} width={60} height={H} fill={wood} />
				<rect x={1440} y={0} width={480} height={H} fill="#15131a" />
				<rect x={1440} y={0} width={480} height={H} fill="#7a6a58" opacity="0.08" />
				{/* peg rail */}
				<rect x={120} y={230} width={1200} height={34} fill={wood} />
				{[420, 760, 1080].map((x) => <rect key={x} x={x - 8} y={244} width={16} height={36} rx={6} fill="#3a2b22" />)}
				{/* dark blue coat */}
				<path d="M 420 270 Q 330 280 300 330 L 250 760 Q 300 790 340 770 L 360 520 L 380 900 L 470 905 L 560 900 L 580 520 L 600 770 Q 640 790 690 760 L 640 330 Q 610 280 520 270 Q 470 300 420 270 Z" fill={navy} />
				<path d="M 470 290 L 470 900" stroke="#000" strokeOpacity="0.3" strokeWidth="3" />
				<path d="M 420 272 L 470 380 L 520 272" fill="none" stroke={navyLit} strokeWidth="10" />
				{[0, 1, 2, 3, 4].map((i) => (
					<g key={i}>
						<circle cx={445} cy={420 + i * 90} r={7} fill="#b8954f" />
						<circle cx={495} cy={420 + i * 90} r={7} fill="#b8954f" />
					</g>
				))}
				{/* cap with a small badge of yellow metal */}
				<path d="M 690 300 Q 690 250 760 246 Q 830 250 830 300 Z" fill={navy} />
				<rect x={690} y={296} width={140} height={22} rx={4} fill={navyLit} />
				<path d="M 700 318 Q 760 350 840 322 L 830 316 Z" fill="#0d0d12" />
				<path d="M 756 268 L 764 268 L 766 292 L 754 292 Z M 752 264 L 768 264 L 760 256 Z" fill="#c9a650" />
				{/* bench with the folded apron, the feather brush and the buff-skin */}
				<rect x={180} y={930} width={1100} height={28} fill={wood} />
				<rect x={220} y={958} width={20} height={122} fill={wood} />
				<rect x={1220} y={958} width={20} height={122} fill={wood} />
				<rect x={760} y={880} width={300} height={52} rx={4} fill={linen} />
				<path d="M 760 900 L 1060 900 M 760 916 L 1060 916" stroke="#000" strokeOpacity="0.12" strokeWidth="2" />
				<g opacity={skin}>
					<rect x={1090} y={898} width={150} height={34} rx={5} fill="#c4a76e" />
					<path d="M 1090 914 L 1240 914" stroke="#000" strokeOpacity="0.15" strokeWidth="2" />
				</g>
				<path d="M 560 924 L 700 900" stroke="#3a2b22" strokeWidth="8" strokeLinecap="round" />
				<path d="M 690 902 Q 740 870 760 896 Q 740 920 690 902 Z" fill="#e8e2d6" opacity="0.8" />
			</g>
		</svg>
	);
};

// ---------- the Fresnel lens, fourth order, seen from inside the lantern ----------
const LENS = {cx: 960, top: 210, belt0: 450, belt1: 620, bottom: 850, half: 230};
const ringsOf = () => {
	const out: {y: number; w: number; belt: boolean; d: number}[] = [];
	const n = 34;
	for (let i = 0; i <= n; i++) {
		const y = lerp(LENS.top + 30, LENS.bottom - 20, i / n);
		let w = LENS.half;
		if (y < LENS.belt0) w = LENS.half * (0.45 + 0.55 * Math.sqrt((y - LENS.top) / (LENS.belt0 - LENS.top)));
		if (y > LENS.belt1) w = LENS.half * (0.6 + 0.4 * Math.sqrt((LENS.bottom - y) / (LENS.bottom - LENS.belt1)));
		const mid = (LENS.belt0 + LENS.belt1) / 2;
		out.push({y, w, belt: y >= LENS.belt0 && y <= LENS.belt1, d: Math.abs(y - mid) / (LENS.bottom - mid)});
	}
	return out;
};
const RINGS = ringsOf();

const Lens: React.FC<{t: number; f: number; fill: number; sheen: number; morning?: boolean}> = ({t, f, fill, sheen, morning}) => {
	const glass = morning ? '#c9d4e0' : c3(t, '#c5ccd8', '#9a9db8', '#4a4f6a');
	const glassDark = morning ? '#6f7d92' : c3(t, '#6f7790', '#4f5070', '#1e2236');
	const bronze = morning ? '#6e5c3e' : c3(t, '#6e5c3e', '#4f4232', '#221d1a');
	const lit = (d: number) => Math.max(0, Math.min(1, (fill * 1.3 - d) / 0.3));
	const h = (LENS.bottom - 20 - (LENS.top + 30)) / (RINGS.length - 1);
	return (
		<g>
			<defs>
				<linearGradient id="lensBand" x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor={glass} />
					<stop offset="1" stopColor={glassDark} />
				</linearGradient>
			</defs>
			{RINGS.map((r, i) => {
				const L = lit(r.d) * fill;
				const shine = 0.5 + 0.5 * Math.sin(i * 0.9 + f / 70);
				const y0 = r.y - h / 2;
				return (
					<g key={i}>
						<rect x={LENS.cx - r.w} y={y0} width={r.w * 2} height={h - 2} fill="url(#lensBand)" opacity={0.42 + 0.1 * shine * sheen} />
						<rect x={LENS.cx - r.w} y={y0} width={r.w * 2} height={1.6} fill="#ffffff" opacity={0.18 + 0.2 * sheen * shine} />
						<rect x={LENS.cx - r.w * 0.62} y={y0} width={r.w * 0.22} height={h - 2} fill="#ffffff" opacity={0.08 + 0.14 * sheen} />
						{L > 0 ? <rect x={LENS.cx - r.w} y={y0} width={r.w * 2} height={h - 2} fill="#ffe2a6" opacity={0.75 * L} /> : null}
					</g>
				);
			})}
			{[-1, -0.5, 0, 0.5, 1].map((u, i) => (
				<path key={i} d={`M ${LENS.cx + u * LENS.half * 0.45} ${LENS.top + 20} L ${LENS.cx + u * LENS.half} ${LENS.belt0} L ${LENS.cx + u * LENS.half} ${LENS.belt1} L ${LENS.cx + u * LENS.half * 0.6} ${LENS.bottom}`}
					stroke={bronze} strokeWidth={i === 0 || i === 4 ? 6 : 3.5} fill="none" />
			))}
			{[LENS.belt0, LENS.belt1].map((y) => <rect key={y} x={LENS.cx - LENS.half - 3} y={y - 4} width={LENS.half * 2 + 6} height={8} fill={bronze} />)}
			<rect x={LENS.cx - LENS.half * 0.6 - 4} y={LENS.bottom - 6} width={LENS.half * 1.2 + 8} height={12} fill={bronze} />
			<path d={`M ${LENS.cx - 46} ${LENS.top + 22} Q ${LENS.cx} ${LENS.top - 26} ${LENS.cx + 46} ${LENS.top + 22} Z`} fill={bronze} />
		</g>
	);
};

// lamp inside the lens: brass font, burner, chimney; flame 0..1
const LensLamp: React.FC<{f: number; inPlace: number; flame: number}> = ({f, inPlace, flame}) => {
	const y = lerp(60, 0, inPlace);
	const k = flicker(f, 3);
	const fh = 14 + 46 * flame;
	return (
		<g transform={`translate(0 ${y})`} opacity={Math.min(1, inPlace * 1.5)}>
			<path d="M 900 700 Q 900 650 920 640 L 1000 640 Q 1020 650 1020 700 Z" fill="#7e6236" />
			<rect x={935} y={600} width={50} height={42} rx={4} fill="#8f7040" />
			<path d="M 942 600 Q 932 560 946 520 L 946 470 L 974 470 L 974 520 Q 988 560 978 600 Z" fill="#dfe4ea" opacity="0.18" stroke="#e8ecf2" strokeOpacity="0.3" strokeWidth="2" />
			{flame > 0 ? (
				<g transform={`translate(960 ${600 - 4}) scale(1 ${k})`}>
					<path d={`M 0 ${-fh} C 9 ${-fh * 0.5} 13 -6 0 0 C -13 -6 -9 ${-fh * 0.5} 0 ${-fh} Z`} fill="url(#lFlame)" />
				</g>
			) : null}
		</g>
	);
};

export const LanternRoom: React.FC<{t: number; f: number; curtains: number; lampIn: number; flame: number; fill: number; match: number; cam: {s: number; cx: number; cy: number}}> = ({
	t, f, curtains, lampIn, flame, fill, match, cam,
}) => {
	const iron = c3(t, '#262b3a', '#171b2a', '#090c17');
	const sheen = Math.max(0, 1 - Math.max(0, t - 0.45) / 0.15);
	const panels = 5;
	const k = flicker(f, 1);
	return (
		<svg width={W} height={H} style={{position: 'absolute'}}>
			<defs>
				<linearGradient id="lFlame" x1="0" y1="1" x2="0" y2="0">
					<stop offset="0" stopColor={P.coal} />
					<stop offset="0.35" stopColor={P.amber} />
					<stop offset="1" stopColor="#ffe9b8" />
				</linearGradient>
				<radialGradient id="lGlow">
					<stop offset="0" stopColor="#ffe6b0" stopOpacity="0.7" />
					<stop offset="0.3" stopColor={P.amber} stopOpacity="0.25" />
					<stop offset="1" stopColor={P.amber} stopOpacity="0" />
				</radialGradient>
				<linearGradient id="lLinen" x1="0" y1="0" x2="1" y2="0">
					<stop offset="0" stopColor="#8f99ae" />
					<stop offset="0.5" stopColor="#aab0bd" />
					<stop offset="1" stopColor="#7f89a0" />
				</linearGradient>
			</defs>
			<g transform={`translate(${W / 2} ${H / 2}) scale(${cam.s}) translate(${-cam.cx} ${-cam.cy})`}>
				{/* the bay and sky through the lantern glass */}
				<Sky t={t} id="lSky" x={-400} y={-300} w={2720} h={1500} horizon={790} />
				{/* iron astragals of the lantern and the parapet below */}
				{[-120, 300, 1620, 2040].map((x) => <rect key={x} x={x} y={-300} width={34} height={1300} fill={iron} />)}
				<rect x={-400} y={150} width={2720} height={18} fill={iron} />
				<rect x={-400} y={880} width={2720} height={500} fill={iron} />
				<rect x={-400} y={870} width={2720} height={14} fill="#000" opacity="0.4" />
				{/* pedestal */}
				<polygon points={pts([[880, 850], [1040, 850], [1080, 1380], [840, 1380]])} fill="#14161f" />
				<circle cx={960} cy={560} r={520} fill="url(#lGlow)" opacity={0.9 * fill * k} style={{mixBlendMode: 'screen'}} />
				<LensLamp f={f} inPlace={lampIn} flame={flame} />
				<Lens t={t} f={f} fill={fill} sheen={sheen} />
				{flame > 0 ? <circle cx={960} cy={570} r={40 + 90 * flame} fill="url(#lGlow)" opacity={Math.min(1, flame * 1.6) * k} style={{mixBlendMode: 'screen'}} /> : null}
				{/* the struck match: a small flame that moves to the wick */}
				{match > 0 && match < 1 ? (
					<g transform={`translate(${lerp(1080, 975, Math.min(1, match * 1.6))} ${lerp(640, 600, Math.min(1, match * 1.6))})`} opacity={Math.sin(match * Math.PI)}>
						<rect x={-2} y={0} width={4} height={40} fill="#d8c9a8" transform="rotate(-30)" />
						<circle r={18} fill="url(#lGlow)" />
						<path d="M 0 -16 C 5 -8 6 -2 0 2 C -6 -2 -5 -8 0 -16 Z" fill="url(#lFlame)" />
					</g>
				) : null}
				{/* linen curtains around the lens, taken down one at a time */}
				{new Array(panels).fill(0).map((_, i) => {
					const u = Math.max(0, Math.min(1, curtains * panels - i));
					if (u >= 1) return null;
					const x = 560 + i * 160 + u * 60;
					const w = 164 * (1 - 0.7 * u);
					return (
						<g key={i} opacity={1 - u}>
							<rect x={x} y={170} width={w} height={720} fill="url(#lLinen)" opacity="0.88" />
							{[0.18, 0.43, 0.67, 0.85].map((d) => <rect key={d} x={x + d * w} y={170} width={6} height={720} fill="#5e6884" opacity="0.18" />)}
						</g>
					);
				})}
				<rect x={520} y={160} width={880} height={10} fill={iron} opacity={curtains < 1 ? 1 : 0.6} />
			</g>
		</svg>
	);
};

// ---------- scene 6, memory: this morning, cleaning the lens ----------
export const LensMemory: React.FC<{f: number; k: number}> = ({f, k}) => {
	const a = f / 22;
	const cx = 960 + Math.cos(a) * 120;
	const cy = 520 + Math.sin(a) * 40;
	return (
		<svg width={W} height={H} style={{position: 'absolute'}}>
			<g transform={`translate(960 540) scale(${1.7 + 0.06 * k}) translate(-960 -500)`}>
				<rect x={-400} y={-300} width={2720} height={1700} fill="#7d8ba0" />
				<rect x={-400} y={700} width={2720} height={700} fill="#56627a" />
				<Lens t={0} f={f} fill={0} sheen={1} morning />
				{/* linen cloth moving in slow circles */}
				<path d={`M ${cx - 60} ${cy - 30} Q ${cx} ${cy - 50} ${cx + 60} ${cy - 26} Q ${cx + 70} ${cy + 20} ${cx + 40} ${cy + 46} Q ${cx - 20} ${cy + 60} ${cx - 64} ${cy + 30} Z`}
					fill="#efe9dc" opacity="0.92" />
				<path d={`M ${cx - 40} ${cy - 10} Q ${cx} ${cy} ${cx + 44} ${cy - 6}`} stroke="#000" strokeOpacity="0.12" strokeWidth="3" fill="none" />
			</g>
			<rect width={W} height={H} fill="#b8c6d8" opacity="0.08" />
		</svg>
	);
};

// ---------- scene 12: the journal, written by lamplight; the writing stays illegible ----------
const scribble = (x0: number, x1: number, y: number, seed: string) => {
	const d: string[] = [`M ${x0} ${y}`];
	let x = x0;
	let i = 0;
	while (x < x1) {
		const letters = 2 + Math.floor(random(`${seed}w${i}`) * 6);
		for (let j = 0; j < letters && x < x1; j++) {
			const w = 7 + random(`${seed}${i}-${j}`) * 7;
			const h = 8 + random(`${seed}h${i}-${j}`) * 10 * (random(`${seed}t${i}-${j}`) > 0.8 ? 1.8 : 1);
			d.push(`C ${x + w * 0.2} ${y - h} ${x + w * 0.9} ${y - h} ${x + w * 0.6} ${y} S ${x + w * 1.1} ${y + 2} ${x + w * 1.2} ${y}`);
			x += w * 1.2;
		}
		x += 14 + random(`${seed}s${i}`) * 8;
		d.push(`M ${x} ${y}`);
		i++;
	}
	return d.join(' ');
};
const JOURNAL_LINES = new Array(15).fill(0).map((_, i) => scribble(380, 1520 - (i % 3) * 120, 300 + i * 38, `j${i}`));
const TODAY = scribble(380, 1240, 300 + 15 * 38, 'today');

export const Journal: React.FC<{t: number; f: number; k: number; write: number}> = ({f, k, write}) => {
	const lamp = flicker(f, 9);
	const paper = '#cdbf9f';
	const lineLen = 2600;
	const tipX = lerp(380, 1240, write);
	return (
		<svg width={W} height={H} style={{position: 'absolute'}}>
			<defs>
				<radialGradient id="jLamp" cx="0.15" cy="0.1" r="0.9">
					<stop offset="0" stopColor={P.amber} stopOpacity="0.38" />
					<stop offset="0.5" stopColor={P.amber} stopOpacity="0.1" />
					<stop offset="1" stopColor="#000" stopOpacity="0" />
				</radialGradient>
			</defs>
			<g transform={drift(k, 900, 560, 0.04)}>
				<rect width={W} height={H} fill="#1d1612" />
				<polygon points={pts([[330, 200], [960, 214], [960, 930], [300, 900]])} fill={paper} />
				<polygon points={pts([[960, 214], [1600, 200], [1630, 900], [960, 930]])} fill={paper} />
				<polygon points={pts([[948, 214], [972, 214], [972, 930], [948, 930]])} fill="#000" opacity="0.15" />
				{new Array(18).fill(0).map((_, i) => <line key={i} x1={330} x2={1610} y1={262 + i * 38 + 12} y2={262 + i * 38 + 12} stroke="#6f7c96" strokeWidth="1.4" opacity="0.4" />)}
				{[420, 700, 1160, 1400].map((x) => <line key={x} x1={x} x2={x} y1={220} y2={910} stroke="#a0544a" strokeWidth="1.2" opacity="0.35" />)}
				{JOURNAL_LINES.map((d, i) => <path key={i} d={d} stroke="#2a2430" strokeWidth="2" fill="none" opacity="0.75" />)}
				<path d={TODAY} stroke="#1a1620" strokeWidth="2.2" fill="none" strokeDasharray={lineLen} strokeDashoffset={lineLen * (1 - write)} />
				{/* inkwell and the pen */}
				<ellipse cx={1720} cy={360} rx={70} ry={22} fill="#0b0a0e" />
				<rect x={1650} y={280} width={140} height={80} rx={14} fill="#16141c" />
				<ellipse cx={1720} cy={280} rx={36} ry={10} fill="#050407" />
				<g transform={`translate(${tipX} ${300 + 15 * 38 - 4})`}>
					<path d="M 0 0 L 160 -150" stroke="#2c2018" strokeWidth="10" strokeLinecap="round" />
					<path d="M 0 0 L 22 -26" stroke="#8c8c94" strokeWidth="6" />
				</g>
				<rect width={W} height={H} fill="url(#jLamp)" opacity={lamp} style={{mixBlendMode: 'screen'}} />
			</g>
		</svg>
	);
};

// ---------- scene 2, rule: a line from the book of instructions ----------
export const RulePage: React.FC<{k: number}> = ({k}) => (
	<svg width={W} height={H} style={{position: 'absolute'}}>
		<g transform={drift(k, 960, 540, 0.04)}>
			<rect width={W} height={H} fill="#1a1712" />
			<polygon points={pts([[440, 90], [1480, 80], [1500, 860], [420, 870]])} fill="#cfc3a6" />
			<polygon points={pts([[440, 90], [1480, 80], [1500, 860], [420, 870]])} fill="none" stroke="#8f8466" strokeWidth="2" />
			{new Array(5).fill(0).map((_, i) => <rect key={i} x={530} y={150 + i * 26} width={860 - (i === 4 ? 300 : 0)} height={7} fill="#7a705c" opacity="0.35" />)}
			{new Array(5).fill(0).map((_, i) => <rect key={i} x={530} y={690 + i * 26} width={860 - (i === 4 ? 420 : 0)} height={7} fill="#7a705c" opacity="0.35" />)}
		</g>
	</svg>
);
~~~~

### `src/Probe.tsx`

~~~~tsx
import React from 'react';
import {
	AbsoluteFill,
	Audio,
	Easing,
	Img,
	interpolate,
	interpolateColors,
	random,
	staticFile,
	useCurrentFrame,
} from 'remotion';
import '@fontsource/cormorant-garamond/600.css';
import '@fontsource/nunito-sans/600.css';
import {P} from './palette';

// 30-second style probe: "A Winter Night in a Lighthouse".
// Flame ident -> pull back into the keeper's window -> wide dusk shot ->
// push in to the tower -> wall opens in section -> keeper climbs -> lamp is lit.
// Everything is drawn here in code; no outside images.

export const W = 1920;
export const H = 1080;
const ease = Easing.inOut(Easing.cubic);
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
export const kf = (f: number, at: number[], v: number[], easing = ease) =>
	interpolate(f, at, v, {...clamp, easing});

// ---------- timeline ----------
const CAM_AT = [60, 190, 380, 545, 760, 900];
const camera = (f: number) => {
	const s = Math.exp(kf(f, CAM_AT, [6, 1.1, 1.22, 2.75, 2.85, 1.7].map(Math.log)));
	const cx = kf(f, CAM_AT, [1072, 1080, 1150, 1300, 1300, 1250]);
	const cy = kf(f, CAM_AT, [548, 520, 480, 395, 380, 440]);
	return {s, cx, cy};
};
const REVEAL = [548, 610];
const CLIMB = [604, 702];
const LADDER = [702, 724];
const LIGHT = 726;

// ---------- tower geometry (world units) ----------
const T = {cx: 1300, topY: 300, baseY: 590, topHalf: 40, baseHalf: 62, wallTop: 7, wallBase: 11};
const tk = (y: number) => (y - T.topY) / (T.baseY - T.topY);
const outerHalf = (y: number) => lerp(T.topHalf, T.baseHalf, tk(y));
const innerHalf = (y: number) => outerHalf(y) - lerp(T.wallTop, T.wallBase, tk(y));
const STAIR_TOP = 346;
const STAIR_BOTTOM = 584;
const TURNS = 2.75;
const LENS = {x: T.cx, y: 262};

const helix = (u: number) => {
	const th = u * TURNS * Math.PI * 2;
	const y = lerp(STAIR_BOTTOM, STAIR_TOP, u);
	const r = innerHalf(y) - 5;
	return {x: T.cx - r * Math.sin(th), y, front: Math.cos(th) > 0};
};

// ---------- small helpers ----------
export const pts = (a: [number, number][]) => a.map((p) => p.join(',')).join(' ');
export const flicker = (f: number, seed: number) =>
	0.88 + 0.06 * Math.sin(f * 0.31 + seed) + 0.04 * Math.sin(f * 0.83 + seed * 2.1) + 0.02 * Math.sin(f * 1.7 + seed * 0.7);

// ---------- sky (screen space) ----------
export const Sky: React.FC<{f: number; dusk: number}> = ({f, dusk}) => {
	const top = interpolateColors(dusk, [0, 1], ['#1a2142', '#0b0f20']);
	const mid = interpolateColors(dusk, [0, 1], ['#2f3561', '#141a33']);
	const low = interpolateColors(dusk, [0, 1], ['#6c6378', '#252a45']);
	const glow = interpolateColors(dusk, [0, 1], ['#b7a596', '#3b3a52']);
	const stars = new Array(150).fill(0).map((_, i) => {
		const x = random(`sx${i}`) * W;
		const y = Math.pow(random(`sy${i}`), 1.4) * H * 0.62;
		const r = 0.5 + random(`sr${i}`) * 1.3;
		const appear = kf(dusk, [0.25 + random(`sa${i}`) * 0.55, 0.85 + random(`sa${i}`) * 0.15], [0, 1]);
		const tw = 0.75 + 0.25 * Math.sin(f / (14 + random(`st${i}`) * 30) + i);
		return <circle key={i} cx={x} cy={y} r={r} fill="#e7e4ef" opacity={appear * tw * (0.35 + 0.5 * random(`so${i}`))} />;
	});
	return (
		<svg width={W} height={H} style={{position: 'absolute'}}>
			<defs>
				<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor={top} />
					<stop offset="0.45" stopColor={mid} />
					<stop offset="0.72" stopColor={low} />
					<stop offset="0.82" stopColor={glow} />
				</linearGradient>
				<radialGradient id="afterglow" cx="0.18" cy="0.8" r="0.6">
					<stop offset="0" stopColor={glow} stopOpacity={0.55 * (1 - dusk)} />
					<stop offset="1" stopColor={glow} stopOpacity="0" />
				</radialGradient>
			</defs>
			<rect width={W} height={H} fill="url(#sky)" />
			<rect width={W} height={H} fill="url(#afterglow)" />
			{stars}
		</svg>
	);
};

// ---------- sea ----------
const Sea: React.FC<{f: number; dusk: number; lamp: number; win: number}> = ({f, dusk, lamp, win}) => {
	const horizon = interpolateColors(dusk, [0, 1], ['#4b5068', '#1c2238']);
	const deep = interpolateColors(dusk, [0, 1], ['#1c2238', '#0b0f1e']);
	const crest = interpolateColors(dusk, [0, 1], ['#9a9cae', '#454c66']);
	const rows = [];
	const R = 46;
	for (let i = 0; i < R; i++) {
		const t = i / R;
		const y = 612 + 560 * Math.pow(t, 1.7);
		const n = 9 + Math.floor(random(`wn${i}`) * 7);
		for (let j = 0; j < n; j++) {
			const len = 18 + 150 * Math.pow(t, 1.1) * random(`wl${i}-${j}`) + 10;
			const x0 = -500 + random(`wx${i}-${j}`) * 3000;
			const drift = Math.sin(f / (70 + 20 * random(`wd${i}`)) + i * 1.3 + j) * (3 + 14 * t);
			const op = (0.06 + 0.2 * random(`wo${i}-${j}`)) * (0.6 + 0.4 * Math.sin(f / 45 + i + j * 0.7));
			rows.push(
				<line key={`${i}-${j}`} x1={x0 + drift} x2={x0 + drift + len} y1={y} y2={y} stroke={crest} strokeWidth={0.6 + 2.4 * t} strokeLinecap="round" opacity={op} />,
			);
		}
	}
	// lamp and window reflections: broken vertical columns of light
	const refl = (x: number, amount: number, width: number, key: string, color: string) => {
		if (amount <= 0.01) return null;
		const out = [];
		for (let i = 0; i < 34; i++) {
			const t = i / 34;
			const y = 662 + 520 * Math.pow(t, 1.5);
			const w = width * (0.4 + 1.6 * t) * (0.5 + random(`${key}w${i}`));
			const jitter = Math.sin(f / 9 + i * 2.3) * (2 + 8 * t);
			const op = amount * (0.25 + 0.55 * random(`${key}o${i}`)) * (0.6 + 0.4 * Math.sin(f / 7 + i * 1.7)) * (1 - t * 0.6);
			out.push(<line key={`${key}${i}`} x1={x - w / 2 + jitter} x2={x + w / 2 + jitter} y1={y} y2={y} stroke={color} strokeWidth={1 + 2 * t} strokeLinecap="round" opacity={op} />);
		}
		return out;
	};
	return (
		<g>
			<defs>
				<linearGradient id="sea" x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor={horizon} />
					<stop offset="0.35" stopColor={deep} />
					<stop offset="1" stopColor={deep} />
				</linearGradient>
			</defs>
			<rect x={-800} y={608} width={3600} height={700} fill="url(#sea)" />
			{rows}
			{refl(T.cx, lamp, 26, 'lr', P.amber)}
			{refl(1072, win * 0.45, 9, 'wr', P.amber)}
		</g>
	);
};

// ---------- far shore with spruce ridge ----------
const FarShore: React.FC<{dusk: number}> = ({dusk}) => {
	const c = interpolateColors(dusk, [0, 1], ['#2b3150', '#121730']);
	const c2 = interpolateColors(dusk, [0, 1], ['#363b5a', '#171c36']);
	const ridge: [number, number][] = [[-800, 612]];
	for (let x = -800; x <= 760; x += 9) {
		const base = 596 - 14 * Math.sin((x + 800) / 520) - 6 * Math.sin(x / 130);
		const tree = random(`tr${x}`) > 0.35 ? 6 + random(`th${x}`) * 13 : 0;
		ridge.push([x, base]);
		if (tree) ridge.push([x + 3, base - tree], [x + 6, base]);
	}
	ridge.push([780, 612]);
	return (
		<g>
			<polygon points={pts([[1720, 612], [1800, 603], [1900, 601], [2010, 604], [2080, 612]])} fill={c2} />
			<polygon points={pts([[2150, 612], [2260, 600], [2400, 598], [2600, 612]])} fill={c2} />
			<polygon points={pts(ridge)} fill={c} />
		</g>
	);
};

// ---------- island, house, outbuildings ----------
const Island: React.FC<{f: number; dusk: number; win: number}> = ({f, dusk, win}) => {
	const snow = interpolateColors(dusk, [0, 1], ['#a9afc4', '#4a5272']);
	const snowLit = interpolateColors(dusk, [0, 1], ['#c7c6cf', '#5b6283']);
	const rock = interpolateColors(dusk, [0, 1], ['#232a40', '#121727']);
	const rockDark = interpolateColors(dusk, [0, 1], ['#181e31', '#0b0f1c']);
	const rockLit = interpolateColors(dusk, [0, 1], ['#343b55', '#1a2034']);
	const clap = interpolateColors(dusk, [0, 1], ['#b9b3aa', '#4a4f64']);
	const clapShade = interpolateColors(dusk, [0, 1], ['#8a8a92', '#33384c']);
	const roof = interpolateColors(dusk, [0, 1], ['#2f3549', '#171c2c']);
	const brick = interpolateColors(dusk, [0, 1], ['#6a4038', '#2e1f22']);
	const top: [number, number][] = [
		[760, 668], [800, 640], [860, 618], [930, 604], [1000, 594], [1040, 592], [1200, 592], [1240, 590],
		[1360, 592], [1450, 596], [1520, 603], [1580, 612], [1640, 626], [1700, 644], [1760, 668],
	];
	const water: [number, number][] = [[1760, 668], [1730, 690], [1660, 702], [1560, 708], [1480, 712], [1300, 716], [1100, 714], [960, 708], [860, 698], [790, 684], [760, 668]];
	const smoke = new Array(9).fill(0).map((_, i) => {
		const life = 260;
		const age = (f + i * (life / 9)) % life;
		const t = age / life;
		return (
			<circle key={i} cx={1156 + 46 * t * t + 4 * Math.sin(age / 20 + i)} cy={466 - 120 * t} r={7 + 26 * t}
				fill="url(#smokePuff)" opacity={0.5 * Math.sin(Math.PI * Math.min(1, t * 1.4))} />
		);
	});
	return (
		<g>
			<defs>
				<radialGradient id="winGlow">
					<stop offset="0" stopColor={P.amber} stopOpacity="0.55" />
					<stop offset="1" stopColor={P.amber} stopOpacity="0" />
				</radialGradient>
				<radialGradient id="smokePuff">
					<stop offset="0" stopColor={interpolateColors(dusk, [0, 1], ['#8a8ea3', '#3f4560'])} stopOpacity="0.55" />
					<stop offset="1" stopColor={interpolateColors(dusk, [0, 1], ['#8a8ea3', '#3f4560'])} stopOpacity="0" />
				</radialGradient>
				<linearGradient id="clapGrad" x1="0" y1="0" x2="1" y2="0">
					<stop offset="0" stopColor={clap} />
					<stop offset="1" stopColor={clapShade} />
				</linearGradient>
			</defs>
			{/* reflection of the rock in the water, broken by swell */}
			{new Array(12).fill(0).map((_, i) => (
				<rect key={i} x={790 + 10 * Math.sin(f / 30 + i)} y={712 + i * 5} width={940 - i * 40} height={3.2} rx={1.5} fill={rockDark}
					opacity={0.55 - i * 0.04} transform={`translate(${i * 20} 0)`} />
			))}
			{/* rock mass */}
			<polygon points={pts([...top, ...water])} fill={rock} />
			<polygon points={pts([[1040, 600], [1200, 600], [1360, 602], [1480, 640], [1460, 712], [1300, 716], [1100, 714], [1010, 690]])} fill={rockDark} opacity="0.35" />
			<polygon points={pts([[1180, 610], [1300, 608], [1260, 668], [1210, 714], [1140, 690]])} fill={rockLit} opacity="0.35" />
			{[0, 1, 2, 3, 4, 5, 6, 7].map((i) => (
				<path key={`c${i}`} d={`M ${860 + i * 105} ${636 + (i % 3) * 6} l ${6 - (i % 2) * 12} ${30 + (i % 4) * 9}`} stroke={rockDark} strokeWidth="1.6" fill="none" opacity="0.7" />
			))}
			<polygon points={pts([[800, 640], [860, 618], [930, 604], [960, 650], [900, 696], [840, 690]])} fill={rockLit} opacity="0.7" />
			<polygon points={pts([[1450, 596], [1520, 603], [1580, 612], [1570, 660], [1500, 710], [1440, 676]])} fill={rockDark} />
			<polygon points={pts([[1580, 612], [1640, 626], [1700, 644], [1700, 690], [1610, 704], [1570, 660]])} fill={rockLit} opacity="0.5" />
			<polygon points={pts([[1000, 594], [1100, 600], [1060, 650], [990, 690], [960, 650]])} fill={rockDark} opacity="0.6" />
			{[0, 1, 2, 3, 4, 5].map((i) => (
				<path key={i} d={`M ${880 + i * 140} ${640 + (i % 3) * 9} q 40 ${-6 + i} 90 ${4 - i}`} stroke={rockDark} strokeWidth="2" fill="none" opacity="0.8" />
			))}
			{/* snow cover on the top */}
			<path d={`M 800 641 L 860 619 L 930 605 L 1000 595 L 1040 593 L 1200 593 L 1240 591 L 1360 593 L 1450 597 L 1520 604 L 1580 613 L 1640 627 L 1700 645
				L 1690 650 L 1630 634 L 1570 621 L 1520 612 L 1440 605 L 1360 600 L 1240 598 L 1200 600 L 1040 600 L 990 603 L 930 613 L 870 627 L 810 648 Z`} fill={snow} />
			<path d="M 940 612 L 990 604 L 1020 606 L 980 618 Z M 1500 612 L 1560 618 L 1540 628 Z" fill={snow} opacity="0.8" />
			{new Array(60).fill(0).map((_, i) => {
				const x = 820 + random(`gx${i}`) * 860;
				const yTop = x < 1040 ? 640 - (x - 800) * 0.2 : x < 1450 ? 596 : 596 + (x - 1450) * 0.22;
				if (x > 1025 && x < 1250) return null;
				const h = 4 + random(`gh${i}`) * 7;
				return <path key={`g${i}`} d={`M ${x} ${yTop + 6} l ${-1.5 + random(`gl${i}`) * 3} ${-h} M ${x + 2} ${yTop + 6} l ${1 + random(`gm${i}`) * 2} ${-h * 0.8}`}
					stroke={interpolateColors(dusk, [0, 1], ['#5c5650', '#24232c'])} strokeWidth="0.8" />;
			})}
			{/* foam */}
			{[0, 1, 2, 3, 4, 5, 6].map((i) => (
				<path key={i} d={`M ${810 + i * 128} ${700 + (i % 2) * 8 - Math.abs(i - 3) * 3} q 30 4 70 1`} stroke="#c9cfdc" strokeWidth="1.4" fill="none"
					opacity={(0.15 + 0.15 * Math.sin(f / 26 + i * 1.9)) * (1 - dusk * 0.5)} />
			))}
			{/* oil house */}
			<rect x={1402} y={568} width={30} height={26} fill={brick} />
			<polygon points={pts([[1398, 569], [1417, 556], [1436, 569]])} fill={roof} />
			<path d="M 1399 568 L 1417 556 L 1435 568" stroke={snowLit} strokeWidth="2.5" fill="none" />
			{/* covered way to the tower */}
			<rect x={1188} y={566} width={56} height={26} fill={clapShade} />
			<polygon points={pts([[1186, 567], [1246, 561], [1246, 567]])} fill={roof} />
			<line x1={1186} y1={565} x2={1246} y2={559} stroke={snowLit} strokeWidth="2.2" />
			{/* keeper's house */}
			<rect x={1030} y={520} width={160} height={72} fill="url(#clapGrad)" />
			{[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((i) => (
				<line key={i} x1={1030} x2={1190} y1={525 + i * 6.5} y2={525 + i * 6.5} stroke={clapShade} strokeWidth="0.6" opacity="0.5" />
			))}
			<polygon points={pts([[1020, 523], [1110, 470], [1200, 523]])} fill={roof} />
			<path d="M 1021 521 L 1110 469 L 1199 521 L 1192 522 L 1110 476 L 1028 522 Z" fill={snowLit} />
			<rect x={1149} y={466} width={14} height={36} fill={brick} />
			<rect x={1147} y={463} width={18} height={5} fill={roof} />
			<rect x={1149} y={461} width={14} height={3} fill={snowLit} />
			{smoke}
			{/* windows: left one lit */}
			<circle cx={1072} cy={548} r={46} fill="url(#winGlow)" opacity={win} />
			<rect x={1063} y={536} width={18} height={24} fill={interpolateColors(win, [0, 1], [P.iron, P.amber])} />
			<rect x={1063} y={536} width={18} height={24} fill="#fff1d2" opacity={0.25 * win} />
			<path d="M 1072 536 V 560 M 1063 548 H 1081" stroke={roof} strokeWidth="1.6" />
			<rect x={1061} y={534} width={22} height={28} fill="none" stroke={clapShade} strokeWidth="2" />
			<rect x={1140} y={536} width={18} height={24} fill={P.iron} />
			<path d="M 1149 536 V 560 M 1140 548 H 1158" stroke={roof} strokeWidth="1.6" />
			<rect x={1102} y={556} width={14} height={36} fill={roof} />
		</g>
	);
};

// ---------- lighthouse exterior ----------
const TowerShell: React.FC<{dusk: number}> = ({dusk}) => {
	const lit = interpolateColors(dusk, [0, 1], ['#d4cdbf', '#575d74']);
	const mid = interpolateColors(dusk, [0, 1], ['#aaa6a3', '#3d4259']);
	const shade = interpolateColors(dusk, [0, 1], ['#6f7183', '#23283d']);
	const {cx, topY, baseY, topHalf, baseHalf} = T;
	return (
		<g>
			<defs>
				<linearGradient id="towerGrad" gradientUnits="userSpaceOnUse" x1={cx - baseHalf} y1="0" x2={cx + baseHalf} y2="0">
					<stop offset="0" stopColor={mid} />
					<stop offset="0.28" stopColor={lit} />
					<stop offset="0.62" stopColor={mid} />
					<stop offset="1" stopColor={shade} />
				</linearGradient>
			</defs>
			<polygon points={pts([[cx - topHalf, topY], [cx + topHalf, topY], [cx + baseHalf, baseY], [cx - baseHalf, baseY]])} fill="url(#towerGrad)" />
			{new Array(28).fill(0).map((_, i) => {
				const y = topY + 8 + i * 10.3;
				return <line key={i} x1={cx - outerHalf(y)} x2={cx + outerHalf(y)} y1={y} y2={y} stroke={shade} strokeWidth="0.5" opacity="0.18" />;
			})}
			{/* small windows and door */}
			<rect x={cx - 4} y={372} width={8} height={13} rx={4} fill={P.iron} opacity="0.85" />
			<rect x={cx - 4.5} y={470} width={9} height={14} rx={4.5} fill={P.iron} opacity="0.85" />
			<rect x={cx - 9} y={560} width={18} height={30} rx={2} fill={P.iron} />
			<rect x={cx - 13} y={556} width={26} height={4} fill={shade} />
		</g>
	);
};

// ---------- cut-away interior ----------
const Interior: React.FC<{f: number; reveal: number; keeper: {x: number; y: number}; hand: number; lamp: number}> = ({
	f, reveal, keeper, hand, lamp,
}) => {
	const {cx, topY, baseY} = T;
	const revealY = lerp(topY, baseY, reveal);
	const inner: [number, number][] = [[cx - innerHalf(topY), topY], [cx + innerHalf(topY), topY], [cx + innerHalf(baseY), baseY], [cx - innerHalf(baseY), baseY]];
	const leftCut: [number, number][] = [[cx - outerHalf(topY), topY], [cx - innerHalf(topY), topY], [cx - innerHalf(baseY), baseY], [cx - outerHalf(baseY), baseY]];
	const rightCut: [number, number][] = leftCut.map(([x, y]) => [2 * cx - x, y]);
	// stair treads along the helix, back half first
	const steps = [];
	const N = 46;
	for (let pass = 0; pass < 2; pass++) {
		for (let i = 0; i <= N; i++) {
			const u = i / N;
			const p = helix(u);
			if ((pass === 0) === p.front) continue;
			steps.push(
				<g key={`${pass}-${i}`} opacity={p.front ? 1 : 0.55}>
					<line x1={cx} y1={p.y + 1.5} x2={p.x} y2={p.y} stroke={p.front ? '#2a2733' : '#1d1b25'} strokeWidth="3" strokeLinecap="round" />
					<line x1={cx} y1={p.y + 0.3} x2={p.x} y2={p.y - 1.2} stroke="#8b7a68" strokeWidth="0.6" opacity={p.front ? 0.6 : 0.25} />
				</g>,
			);
		}
	}
	const rail = new Array(121).fill(0).map((_, i) => {
		const p = helix(i / 120);
		return `${i ? 'L' : 'M'} ${p.x.toFixed(1)} ${(p.y - 9).toFixed(1)}`;
	}).join(' ');
	const handGlow = hand * flicker(f, 3);
	return (
		<g>
			<defs>
				<clipPath id="revealClip">
					<rect x={cx - 80} y={topY - 2} width={160} height={revealY - topY + 2} />
				</clipPath>
				<clipPath id="innerClip">
					<polygon points={pts(inner)} />
				</clipPath>
				<pattern id="hatch" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
					<rect width="4" height="4" fill="#4a3a3a" />
					<line x1="0" y1="0" x2="0" y2="4" stroke="#2a2026" strokeWidth="1.4" />
				</pattern>
				<radialGradient id="handLight">
					<stop offset="0" stopColor="#f6d39a" stopOpacity="0.85" />
					<stop offset="0.35" stopColor={P.amber} stopOpacity="0.35" />
					<stop offset="1" stopColor={P.amber} stopOpacity="0" />
				</radialGradient>
				<radialGradient id="topLight" cx="0.5" cy="0">
					<stop offset="0" stopColor="#f6d39a" stopOpacity="0.7" />
					<stop offset="1" stopColor={P.amber} stopOpacity="0" />
				</radialGradient>
				<linearGradient id="wallInside" x1="0" y1="0" x2="1" y2="0">
					<stop offset="0" stopColor="#2b2833" />
					<stop offset="0.5" stopColor="#3a3540" />
					<stop offset="1" stopColor="#24222c" />
				</linearGradient>
			</defs>
			<g clipPath="url(#revealClip)">
				<g clipPath="url(#innerClip)">
					<polygon points={pts(inner)} fill="url(#wallInside)" />
					{/* courses of the inner brick lining */}
					{new Array(30).fill(0).map((_, i) => (
						<line key={i} x1={cx - 70} x2={cx + 70} y1={topY + 6 + i * 9.6} y2={topY + 6 + i * 9.6} stroke="#1c1a22" strokeWidth="0.7" opacity="0.6" />
					))}
					{/* window niches in the back wall: cold evening light */}
					{[[-17, 404], [15, 498]].map(([dx, y], i) => (
						<g key={`n${i}`}>
							<rect x={cx + dx - 5} y={y} width={10} height={17} rx={5} fill="#141220" />
							<rect x={cx + dx - 3.5} y={y + 2} width={7} height={13} rx={3.5} fill="#56608a" opacity={0.75} />
						</g>
					))}
					{/* watch room: floor, oil cans, log book, clock */}
					<rect x={cx - 50} y={STAIR_TOP} width={100} height={4} fill="#17151d" />
					<rect x={cx - 38} y={topY} width={76} height={6} fill="#17151d" />
					<rect x={cx - 3} y={topY + 6} width={6} height={STAIR_TOP - topY - 6} fill="#1a1820" />
					{[0, 1, 2].map((i) => (
						<g key={i}>
							<rect x={cx + 14 + i * 7} y={STAIR_TOP - 11} width={6} height={11} rx={1} fill="#8c7444" />
							<rect x={cx + 15 + i * 7} y={STAIR_TOP - 13} width={2} height={3} fill="#8c7444" />
						</g>
					))}
					<rect x={cx - 30} y={STAIR_TOP - 12} width={18} height={2} fill="#2c2632" />
					<rect x={cx - 28} y={STAIR_TOP - 10} width={2} height={10} fill="#2c2632" />
					<rect x={cx - 16} y={STAIR_TOP - 10} width={2} height={10} fill="#2c2632" />
					<rect x={cx - 27} y={STAIR_TOP - 15} width={11} height={3} fill="#d7c9ae" />
					<circle cx={cx + 22} cy={topY + 22} r={4.5} fill="#d7c9ae" stroke="#5a4a3a" strokeWidth="0.8" />
					<path d={`M ${cx + 22} ${topY + 22} v -3 M ${cx + 22} ${topY + 22} h 2`} stroke="#2a2026" strokeWidth="0.6" />
					{/* stair: newel, treads, handrail */}
					<rect x={cx - 1.6} y={STAIR_TOP} width={3.2} height={STAIR_BOTTOM - STAIR_TOP + 6} fill="#16141c" />
					{steps}
					<path d={rail} stroke="#16141c" strokeWidth="1.1" fill="none" opacity="0.9" />
					{/* light: hand lamp follows the keeper, lantern light falls through the hatch */}
					<circle cx={keeper.x + 6} cy={keeper.y - 11} r={78} fill="url(#handLight)" opacity={handGlow} style={{mixBlendMode: 'screen'}} />
					<ellipse cx={cx} cy={topY + 6} rx={60} ry={70} fill="url(#topLight)" opacity={lamp * 0.8} style={{mixBlendMode: 'screen'}} />
				</g>
				{/* wall section faces */}
				<polygon points={pts(leftCut)} fill="url(#hatch)" />
				<polygon points={pts(rightCut)} fill="url(#hatch)" />
				<polygon points={pts(leftCut)} fill="#000" opacity="0.25" />
			</g>
			{/* the moving edge of the cut */}
			{reveal > 0 && reveal < 1 ? (
				<line x1={cx - outerHalf(revealY) - 2} x2={cx + outerHalf(revealY) + 2} y1={revealY} y2={revealY} stroke="#e9d9bd" strokeWidth="1" opacity="0.5" />
			) : null}
		</g>
	);
};

// ---------- the keeper: a silhouette without a face ----------
export const Keeper: React.FC<{x: number; y: number; step: number; hand: number; f: number; facing: number}> = ({x, y, step, hand, f, facing}) => {
	const sw = Math.sin(step) * 1.6;
	return (
		<g transform={`translate(${x} ${y}) scale(${facing} 1)`}>
			<path d={`M -2.6 -7 L ${-3 + sw} 0 L ${-1 + sw} 0 L -0.4 -7 Z M 0.6 -7 L ${1.2 - sw} 0 L ${3.2 - sw} 0 L 2.6 -7 Z`} fill="#0a0c14" />
			<path d="M -4.2 -17.5 Q -5.6 -11 -5.4 -6.5 L 5 -6.5 Q 5.2 -12 4 -17.5 Q 0 -19.6 -4.2 -17.5 Z" fill="#0a0c14" />
			<circle cx={0} cy={-20.6} r={2.7} fill="#0a0c14" />
			<path d="M -3.4 -22 L 3.4 -22 L 3.6 -21 L -3.6 -21 Z M -2.6 -22 Q 0 -25 2.6 -22 Z" fill="#0a0c14" />
			<path d="M 3.6 -16.5 L 6.6 -12.5 L 6.8 -11.2" stroke="#0a0c14" strokeWidth="1.8" strokeLinecap="round" fill="none" />
			<g opacity={hand}>
				<rect x={5.6} y={-11.2} width={2.6} height={3.6} rx={0.6} fill="#2a2018" />
				<circle cx={6.9} cy={-9.3} r={1.1} fill="#ffe3a6" opacity={flicker(f, 5)} />
			</g>
		</g>
	);
};

// ---------- lantern, gallery and the Fresnel lens ----------
const Lantern: React.FC<{f: number; dusk: number; lamp: number}> = ({f, dusk, lamp}) => {
	const {cx} = T;
	const iron = interpolateColors(dusk, [0, 1], ['#22283a', '#0e1220']);
	const snowLit = interpolateColors(dusk, [0, 1], ['#c7c6cf', '#5b6283']);
	const glassDark = interpolateColors(dusk, [0, 1], ['#3d4566', '#1a2038']);
	const L = lamp * flicker(f, 1);
	const prism = interpolateColors(L, [0, 1], ['#6f7f99', '#fff0cc']);
	const rings = [];
	for (let i = 0; i < 7; i++) {
		const yU = LENS.y - 4 - i * 1.7;
		const yD = LENS.y + 4 + i * 1.7;
		const w = 9.5 - i * 1.05;
		rings.push(<line key={`u${i}`} x1={cx - w} x2={cx + w} y1={yU} y2={yU} stroke={prism} strokeWidth="0.9" opacity={0.55 + 0.4 * L} />);
		rings.push(<line key={`d${i}`} x1={cx - w} x2={cx + w} y1={yD} y2={yD} stroke={prism} strokeWidth="0.9" opacity={0.55 + 0.4 * L} />);
	}
	const astragals = [-1, -0.62, -0.2, 0.2, 0.62, 1].map((k) => cx + 31 * k);
	return (
		<g>
			<defs>
				<radialGradient id="lensCore">
					<stop offset="0" stopColor="#fffaf0" stopOpacity="1" />
					<stop offset="0.3" stopColor="#ffe2a0" stopOpacity="0.9" />
					<stop offset="1" stopColor={P.amber} stopOpacity="0" />
				</radialGradient>
				<radialGradient id="halo">
					<stop offset="0" stopColor="#ffe6b0" stopOpacity="0.75" />
					<stop offset="0.25" stopColor={P.amber} stopOpacity="0.28" />
					<stop offset="1" stopColor={P.amber} stopOpacity="0" />
				</radialGradient>
				<radialGradient id="band" cx="0.5" cy="0.5" r="0.5">
					<stop offset="0" stopColor="#ffeac0" stopOpacity="0.7" />
					<stop offset="0.12" stopColor={P.amber} stopOpacity="0.32" />
					<stop offset="1" stopColor={P.amber} stopOpacity="0" />
				</radialGradient>
				<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1">
					<stop offset="0" stopColor={glassDark} />
					<stop offset="0.5" stopColor={interpolateColors(dusk, [0, 1], ['#59628a', '#252c4a'])} />
					<stop offset="1" stopColor={glassDark} />
				</linearGradient>
			</defs>
			{/* cornice and gallery deck */}
			<polygon points={pts([[cx - 40, 300], [cx + 40, 300], [cx + 48, 294], [cx - 48, 294]])} fill={iron} />
			<rect x={cx - 60} y={289} width={120} height={5} fill={iron} />
			<rect x={cx - 60} y={287.4} width={120} height={2} fill={snowLit} />
			{/* glazing */}
			<rect x={cx - 31} y={244} width={62} height={36} fill="url(#glass)" />
			<rect x={cx - 31} y={244} width={62} height={36} fill={P.amber} opacity={0.45 * L} />
			{/* lens */}
			<rect x={cx - 10} y={LENS.y - 16} width={20} height={32} fill="#10131f" opacity={0.6 * (1 - L)} />
			{rings}
			<rect x={cx - 10} y={LENS.y - 3.5} width={20} height={7} fill={prism} opacity={0.35 + 0.65 * L} />
			<line x1={cx - 10} x2={cx - 10} y1={LENS.y - 16} y2={LENS.y + 16} stroke="#6b5a3a" strokeWidth="0.8" />
			<line x1={cx + 10} x2={cx + 10} y1={LENS.y - 16} y2={LENS.y + 16} stroke="#6b5a3a" strokeWidth="0.8" />
			<line x1={cx} x2={cx} y1={LENS.y - 16} y2={LENS.y + 16} stroke="#6b5a3a" strokeWidth="0.5" opacity="0.7" />
			<circle cx={cx} cy={LENS.y} r={14 * L + 0.01} fill="url(#lensCore)" />
			{/* lantern frame */}
			{astragals.map((x, i) => (
				<line key={i} x1={x} x2={x} y1={244} y2={280} stroke={iron} strokeWidth={i === 0 || i === 5 ? 2.4 : 1.3} />
			))}
			<line x1={cx - 31} x2={cx + 31} y1={262} y2={262} stroke={iron} strokeWidth="0.9" opacity="0.8" />
			<rect x={cx - 34} y={280} width={68} height={9} fill={iron} />
			<rect x={cx - 34} y={241} width={68} height={3.5} fill={iron} />
			{/* dome, ventilator, rod */}
			<path d={`M ${cx - 36} 242 Q ${cx} 210 ${cx + 36} 242 Z`} fill={iron} />
			<path d={`M ${cx - 33} 240 Q ${cx - 14} 222 ${cx} 221`} stroke={snowLit} strokeWidth="2.4" fill="none" opacity="0.85" />
			<circle cx={cx} cy={218} r={5} fill={iron} />
			<line x1={cx} x2={cx} y1={213} y2={196} stroke={iron} strokeWidth="1.2" />
			{/* gallery railing */}
			<line x1={cx - 60} x2={cx + 60} y1={276} y2={276} stroke={iron} strokeWidth="1.4" />
			<line x1={cx - 60} x2={cx + 60} y1={282} y2={282} stroke={iron} strokeWidth="0.7" />
			{new Array(16).fill(0).map((_, i) => (
				<line key={i} x1={cx - 60 + i * 8} x2={cx - 60 + i * 8} y1={276} y2={289} stroke={iron} strokeWidth="0.8" />
			))}
			{/* light outside: halo and the flat band a fixed lens throws to the horizon */}
			<ellipse cx={cx} cy={LENS.y} rx={1100} ry={16} fill="url(#band)" opacity={0.75 * L} style={{mixBlendMode: 'screen'}} />
			<circle cx={cx} cy={LENS.y} r={110} fill="url(#halo)" opacity={0.85 * L} style={{mixBlendMode: 'screen'}} />
		</g>
	);
};

// ---------- falling snow (screen space) ----------
const Snow: React.FC<{f: number; amount: number}> = ({f, amount}) => (
	<svg width={W} height={H} style={{position: 'absolute'}}>
		{new Array(170).fill(0).map((_, i) => {
			const depth = random(`fd${i}`);
			const speed = 0.35 + depth * 1.1;
			const y = ((random(`fy${i}`) * (H + 80) + f * speed) % (H + 80)) - 40;
			const x = random(`fx${i}`) * W + Math.sin(f / (40 + 30 * random(`fs${i}`)) + i) * (6 + 14 * depth) - f * 0.12 * depth;
			const xx = ((x % W) + W) % W;
			return <circle key={i} cx={xx} cy={y} r={0.7 + depth * 2.1} fill="#dfe4ee" opacity={amount * (0.25 + 0.5 * depth)} />;
		})}
	</svg>
);

// ---------- flame ident ----------
export const Flame: React.FC<{f: number; size: number; opacity: number}> = ({f, size, opacity}) => {
	const k = flicker(f, 7);
	const sway = Math.sin(f / 11) * 0.06;
	return (
		<svg width={W} height={H} style={{position: 'absolute', opacity}}>
			<defs>
				<radialGradient id="identGlow">
					<stop offset="0" stopColor={P.amber} stopOpacity="0.45" />
					<stop offset="1" stopColor={P.amber} stopOpacity="0" />
				</radialGradient>
				<linearGradient id="flameFill" x1="0" y1="1" x2="0" y2="0">
					<stop offset="0" stopColor={P.coal} />
					<stop offset="0.35" stopColor={P.amber} />
					<stop offset="1" stopColor="#ffe9b8" />
				</linearGradient>
			</defs>
			<g transform={`translate(${W / 2} ${H / 2}) scale(${size / 100})`}>
				<circle r={150 * k} fill="url(#identGlow)" />
				<g transform={`skewX(${sway * 40}) scale(1 ${k})`}>
					<path d="M 0 -62 C 18 -30 30 -10 30 14 C 30 34 16 46 0 46 C -16 46 -30 34 -30 14 C -30 -10 -18 -30 0 -62 Z" fill="url(#flameFill)" />
					<path d="M 0 -18 C 8 -2 12 8 12 18 C 12 28 6 34 0 34 C -6 34 -12 28 -12 18 C -12 8 -8 -2 0 -18 Z" fill="#fff6e0" opacity="0.85" />
				</g>
				<rect x={-3} y={46} width={6} height={10} fill="#2b2420" />
			</g>
		</svg>
	);
};

export type Cam = {s: number; cx: number; cy: number};

// Everything the world needs at a given frame of the probe timeline.
export const stateAt = (f: number) => {
	const dusk = kf(f, [60, 900], [0, 1], Easing.inOut(Easing.quad));
	const reveal = kf(f, REVEAL, [0, 1]);
	const lamp = kf(f, [LIGHT, LIGHT + 8, LIGHT + 14, LIGHT + 40], [0, 0.55, 0.35, 1], Easing.out(Easing.quad));
	// keeper: up the spiral stair, then the ladder into the lantern
	const u = kf(f, CLIMB, [0, 1], Easing.inOut(Easing.sin));
	const onStair = helix(u);
	const ladder = kf(f, LADDER, [0, 1]);
	const keeper = f < LADDER[0]
		? {x: onStair.x, y: onStair.y}
		: {x: lerp(onStair.x, T.cx - 17, ladder), y: lerp(STAIR_TOP, 281, ladder)};
	const facing = f < LADDER[0] ? (Math.cos(u * TURNS * Math.PI * 2 + Math.PI / 2) > 0 ? 1 : -1) : 1;
	const hand = kf(f, [LIGHT + 10, LIGHT + 40], [1, 0]);
	const inLantern = f >= LADDER[1] - 6;
	return {f, dusk, reveal, lamp, keeper, facing, hand, inLantern, win: 1, cam: camera(f) as Cam};
};
export type SceneState = ReturnType<typeof stateAt>;

export const World: React.FC<{st: SceneState}> = ({st}) => {
	const {f, dusk, reveal, lamp, keeper, facing, hand, inLantern, win, cam} = st;
	const world = `translate(${W / 2} ${H / 2}) scale(${cam.s}) translate(${-cam.cx} ${-cam.cy})`;
	return (
		<>
			<Sky f={f} dusk={dusk} />
			<svg width={W} height={H} style={{position: 'absolute'}}>
				<g transform={world}>
					<FarShore dusk={dusk} />
					<Sea f={f} dusk={dusk} lamp={lamp} win={win} />
					<Island f={f} dusk={dusk} win={win} />
					<TowerShell dusk={dusk} />
					<Interior f={f} reveal={reveal} keeper={keeper} hand={hand} lamp={lamp} />
					{!inLantern && reveal > 0.3 ? (
						<Keeper x={keeper.x} y={keeper.y} step={f / 3.2} hand={hand} f={f} facing={facing} />
					) : null}
					<Lantern f={f} dusk={dusk} lamp={lamp} />
					{inLantern ? <Keeper x={keeper.x} y={keeper.y} step={0} hand={hand} f={f} facing={1} /> : null}
				</g>
			</svg>
			<Snow f={f} amount={0.9} />
		</>
	);
};

export const Finish: React.FC = () => (
	<>
		<AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(5,7,15,0.55) 100%)'}} />
		<Img src={staticFile('grain.png')} style={{display: 'none'}} />
		<AbsoluteFill style={{backgroundImage: `url(${staticFile('grain.png')})`, backgroundRepeat: 'repeat', opacity: 0.07, mixBlendMode: 'overlay'}} />
	</>
);

export const Probe: React.FC = () => {
	const f = useCurrentFrame();
	const st = stateAt(f);
	const worldIn = kf(f, [62, 118], [0, 1], Easing.out(Easing.quad));
	const flameOpacity = kf(f, [0, 14, 96, 128], [0, 1, 1, 0]);
	const flameSize = 22 * st.cam.s * 1.7;
	const identText = kf(f, [12, 30, 52, 70], [0, 1, 1, 0]);
	const titleIn = kf(f, [205, 245, 330, 368], [0, 1, 1, 0]);
	const endFade = kf(f, [862, 900], [0, 0.55]);

	return (
		<AbsoluteFill style={{backgroundColor: P.night}}>
			<AbsoluteFill style={{opacity: worldIn}}>
				<World st={st} />
			</AbsoluteFill>
			<Flame f={f} size={flameSize} opacity={flameOpacity} />
			<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
				<div style={{marginTop: 340, opacity: identText, color: P.plaster, fontFamily: 'Nunito Sans', fontWeight: 600, fontSize: 20, letterSpacing: 9}}>
					LANTERN LIBRARY
				</div>
			</AbsoluteFill>
			<AbsoluteFill style={{padding: '0 0 120px 140px', justifyContent: 'flex-end', opacity: titleIn}}>
				<div style={{transform: `translateY(${(1 - titleIn) * 14}px)`}}>
					<div style={{color: P.plaster, opacity: 0.72, fontFamily: 'Nunito Sans', fontWeight: 600, fontSize: 19, letterSpacing: 6}}>
						ONE NIGHT IN · MAINE, 1891
					</div>
					<div style={{color: P.plaster, fontFamily: 'Cormorant Garamond', fontWeight: 600, fontSize: 84, lineHeight: 1.05, marginTop: 10, textShadow: '0 2px 24px rgba(10,12,24,0.6)'}}>
						A Winter Night in a Lighthouse
					</div>
				</div>
			</AbsoluteFill>
			<Finish />
			<AbsoluteFill style={{backgroundColor: '#05070f', opacity: endFade}} />
			<Audio src={staticFile('ambience.wav')} />
		</AbsoluteFill>
	);
};
~~~~

### `src/Root.tsx`

~~~~tsx
import React from 'react';
import {Composition, Still} from 'remotion';
import {Probe} from './Probe';
import {Thumbnail} from './Thumbnails';
import {FortFrame} from './FortPoint';
import {Chapter, CHAPTER_FRAMES} from './Chapter';
import {Avatar, Banner} from './Branding';

export const RemotionRoot: React.FC = () => (
	<>
		<Composition id="LighthouseProbe" component={Probe} durationInFrames={900} fps={30} width={1920} height={1080} />
		<Composition id="Chapter1" component={Chapter} durationInFrames={CHAPTER_FRAMES} fps={30} width={1920} height={1080} defaultProps={{audio: true, voice: false, captions: true}} />
		{['A', 'B', 'C'].map((o) => (
			<Still key={o} id={`Thumb${o}`} component={Thumbnail} defaultProps={{option: o}} width={1920} height={1080} />
		))}
		{['K1', 'K2', 'K3', 'K4'].map((k) => (
			<Still key={k} id={`Fort${k}`} component={FortFrame} defaultProps={{frame: k}} width={1920} height={1080} />
		))}
		<Still id="Avatar" component={Avatar} defaultProps={{bg: true}} width={800} height={800} />
		<Still id="Banner" component={Banner} defaultProps={{layer: 'all' as const, check: false}} width={1920} height={1080} />
		<Still id="BannerBackground" component={Banner} defaultProps={{layer: 'bg' as const, check: false}} width={1920} height={1080} />
		<Still id="BannerText" component={Banner} defaultProps={{layer: 'text' as const, check: false}} width={1920} height={1080} />
		<Still id="BannerSafeAreaCheck" component={Banner} defaultProps={{layer: 'all' as const, check: true}} width={1920} height={1080} />
	</>
);
~~~~

### `src/Thumbnails.tsx`

~~~~tsx
import React from 'react';
import {AbsoluteFill} from 'remotion';
import {FortWorld, type FortState} from './FortPoint';
import {Finish} from './Probe';
import {P} from './palette';

// Cover options for Fort Point, January 1892: one lit window or the cut-away
// on a dark field, 3-4 words, no arrows.
const OPTIONS: Record<string, {st: FortState; words: string; small: string; side: 'left' | 'right'}> = {
	A: {st: {t: 0.9, lamp: 1, cut: 0, f: 700, cam: {s: 1.9, cx: 840, cy: 560}}, words: 'One Winter Night, 1892', small: 'FORT POINT, MAINE · SLEEP STORY', side: 'left'},
	B: {st: {t: 0.85, lamp: 1, cut: 0, f: 760, cam: {s: 6, cx: 1060, cy: 448}, keeper: {x: 1133, y: 453, hand: 0, facing: 1}}, words: 'Light the Lamp', small: 'FORT POINT, MAINE · 1892', side: 'left'},
	C: {st: {t: 0.8, lamp: 1, cut: 1, f: 620, cam: {s: 2.7, cx: 1060, cy: 560}, keeper: {x: 1124, y: 627, hand: 0.8, facing: 1}}, words: "The Keeper's Night", small: 'MAINE · 1892 · SLEEP STORY', side: 'left'},
};

export const Thumbnail: React.FC<{option: string}> = ({option}) => {
	const o = OPTIONS[option];
	return (
		<AbsoluteFill style={{backgroundColor: P.night}}>
			<FortWorld st={o.st} />
			<AbsoluteFill
				style={{
					background: o.side === 'left'
						? 'linear-gradient(90deg, rgba(8,10,22,0.85) 0%, rgba(8,10,22,0.5) 36%, rgba(8,10,22,0) 58%)'
						: 'linear-gradient(270deg, rgba(8,10,22,0.85) 0%, rgba(8,10,22,0.5) 36%, rgba(8,10,22,0) 58%)',
				}}
			/>
			<AbsoluteFill style={{justifyContent: 'center', alignItems: o.side === 'left' ? 'flex-start' : 'flex-end', padding: '0 110px'}}>
				<div style={{maxWidth: 820, textAlign: o.side}}>
					<div style={{color: P.plaster, fontFamily: 'Cormorant Garamond', fontWeight: 600, fontSize: 150, lineHeight: 0.98, textShadow: '0 4px 40px rgba(5,7,15,0.8)'}}>
						{o.words}
					</div>
					<div style={{color: P.plaster, opacity: 0.8, marginTop: 28, fontFamily: 'Nunito Sans', fontWeight: 600, fontSize: 30, letterSpacing: 8, whiteSpace: 'nowrap'}}>
						{o.small}
					</div>
				</div>
			</AbsoluteFill>
			<Finish />
		</AbsoluteFill>
	);
};
~~~~

### `src/chapter1.json`

~~~~json
{
 "wpm": 115,
 "duration": 1417.3,
 "scenes": [
  {
   "n": 1,
   "title": "Вступление",
   "start": 3.0,
   "end": 87.39
  },
  {
   "n": 2,
   "title": "Мыс днём",
   "start": 87.39,
   "end": 288.13
  },
  {
   "n": 3,
   "title": "Правило заката",
   "start": 288.13,
   "end": 379.22
  },
  {
   "n": 4,
   "title": "Кто держит свет",
   "start": 379.22,
   "end": 445.39
  },
  {
   "n": 5,
   "title": "Лампа греется на кухне",
   "start": 445.39,
   "end": 532.91
  },
  {
   "n": 6,
   "title": "Масло днём",
   "start": 532.91,
   "end": 647.91
  },
  {
   "n": 7,
   "title": "Форма и фартук",
   "start": 647.91,
   "end": 751.43
  },
  {
   "n": 8,
   "title": "Через мастерскую в башню",
   "start": 751.43,
   "end": 827.43
  },
  {
   "n": 9,
   "title": "Занавески",
   "start": 827.43,
   "end": 937.17
  },
  {
   "n": 10,
   "title": "Линза",
   "start": 937.17,
   "end": 1018.43
  },
  {
   "n": 11,
   "title": "Зажечь лампу",
   "start": 1018.43,
   "end": 1121.13
  },
  {
   "n": 12,
   "title": "Свет над водой",
   "start": 1121.13,
   "end": 1225.17
  },
  {
   "n": 13,
   "title": "Ночь впереди",
   "start": 1225.17,
   "end": 1356.0
  },
  {
   "n": 14,
   "title": "Конец главы",
   "start": 1356.0,
   "end": 1417.3
  }
 ],
 "cues": [
  {
   "start": 3.0,
   "end": 4.57,
   "text": "Part one. Dusk.",
   "scene": 1
  },
  {
   "start": 6.57,
   "end": 13.87,
   "text": "It is a Saturday in the middle of January, in the year eighteen ninety-two.",
   "scene": 1
  },
  {
   "start": 13.87,
   "end": 23.26,
   "text": "You are on the coast of Maine, at the place where the Penobscot River opens into the bay.",
   "scene": 1
  },
  {
   "start": 25.26,
   "end": 33.09,
   "text": "There is a small light station here, on a point of land called Fort Point.",
   "scene": 1
  },
  {
   "start": 33.09,
   "end": 37.78,
   "text": "And for this one night, you are its keeper.",
   "scene": 1
  },
  {
   "start": 39.78,
   "end": 43.96,
   "text": "You have one task before the day ends.",
   "scene": 1
  },
  {
   "start": 43.96,
   "end": 52.3,
   "text": "When the sun goes down, the lamp at the top of the tower must be burning.",
   "scene": 1
  },
  {
   "start": 54.3,
   "end": 57.43,
   "text": "Nothing else is required of you.",
   "scene": 1
  },
  {
   "start": 57.43,
   "end": 59.52,
   "text": "There is no hurry.",
   "scene": 1
  },
  {
   "start": 59.52,
   "end": 67.87,
   "text": "There is only the work, and the evening, and the long winter night that comes after.",
   "scene": 1
  },
  {
   "start": 70.87,
   "end": 74.52,
   "text": "So let the day settle around you.",
   "scene": 1
  },
  {
   "start": 74.52,
   "end": 76.61,
   "text": "Let your shoulders drop.",
   "scene": 1
  },
  {
   "start": 76.61,
   "end": 83.39,
   "text": "We will walk through this evening slowly, one small thing at a time.",
   "scene": 1
  },
  {
   "start": 87.39,
   "end": 92.09,
   "text": "The afternoon light in January is low and thin.",
   "scene": 2
  },
  {
   "start": 92.09,
   "end": 99.91,
   "text": "It comes across the water at a long angle, and it does not stay long.",
   "scene": 2
  },
  {
   "start": 101.91,
   "end": 107.13,
   "text": "Look at the station from the edge of the point.",
   "scene": 2
  },
  {
   "start": 107.13,
   "end": 112.35,
   "text": "There is the keeper's house, a wooden house painted white,",
   "scene": 2
  },
  {
   "start": 112.35,
   "end": 116.0,
   "text": "with its chimney and its small windows.",
   "scene": 2
  },
  {
   "start": 118.0,
   "end": 125.3,
   "text": "And joined to the house, by a narrow room of brick, is the tower.",
   "scene": 2
  },
  {
   "start": 125.3,
   "end": 130.0,
   "text": "It is not tall, and it is not round.",
   "scene": 2
  },
  {
   "start": 130.0,
   "end": 137.83,
   "text": "It is square, built of brick and painted white, with the glass lantern on top.",
   "scene": 2
  },
  {
   "start": 139.83,
   "end": 143.48,
   "text": "That narrow brick room is the workroom.",
   "scene": 2
  },
  {
   "start": 143.48,
   "end": 153.39,
   "text": "It means that you can walk from the warm kitchen to the foot of the tower without stepping outside.",
   "scene": 2
  },
  {
   "start": 153.39,
   "end": 158.61,
   "text": "On a night like this one, that is a gift.",
   "scene": 2
  },
  {
   "start": 161.61,
   "end": 166.83,
   "text": "A light has stood on this point since eighteen thirty-six.",
   "scene": 2
  },
  {
   "start": 166.83,
   "end": 173.09,
   "text": "The brick tower you are looking at was built in eighteen fifty-seven.",
   "scene": 2
  },
  {
   "start": 173.09,
   "end": 182.48,
   "text": "So it is already older than you might think, and it has seen many winters like this one.",
   "scene": 2
  },
  {
   "start": 185.48,
   "end": 194.87,
   "text": "A little way off, about two hundred and fifty feet to the east and north, stands a second,",
   "scene": 2
  },
  {
   "start": 194.87,
   "end": 195.91,
   "text": "smaller tower.",
   "scene": 2
  },
  {
   "start": 195.91,
   "end": 202.17,
   "text": "It is made of wood, shaped like a pyramid, and painted white.",
   "scene": 2
  },
  {
   "start": 202.17,
   "end": 205.3,
   "text": "It is only two years old.",
   "scene": 2
  },
  {
   "start": 207.3,
   "end": 210.43,
   "text": "Inside it hangs the fog bell.",
   "scene": 2
  },
  {
   "start": 210.43,
   "end": 218.78,
   "text": "When fog comes in over the bay, a machine strikes the bell, once every ten seconds,",
   "scene": 2
  },
  {
   "start": 218.78,
   "end": 225.57,
   "text": "so that ships can hear the point even when they cannot see it.",
   "scene": 2
  },
  {
   "start": 228.57,
   "end": 234.83,
   "text": "The book of instructions has rules for bell machines like this one.",
   "scene": 2
  },
  {
   "start": 234.83,
   "end": 239.52,
   "text": "Never leave the machine alone while it is running;",
   "scene": 2
  },
  {
   "start": 239.52,
   "end": 244.22,
   "text": "someone competent must be in constant attendance upon it.",
   "scene": 2
  },
  {
   "start": 244.22,
   "end": 251.52,
   "text": "And always take off the winding crank as soon as the machine is wound.",
   "scene": 2
  },
  {
   "start": 254.52,
   "end": 258.7,
   "text": "Tonight, we will imagine the air is clear.",
   "scene": 2
  },
  {
   "start": 258.7,
   "end": 261.83,
   "text": "The bell will likely stay silent.",
   "scene": 2
  },
  {
   "start": 264.83,
   "end": 269.0,
   "text": "Near the station there is a large hotel,",
   "scene": 2
  },
  {
   "start": 269.0,
   "end": 274.74,
   "text": "built in the eighteen seventies for summer guests from the cities.",
   "scene": 2
  },
  {
   "start": 274.74,
   "end": 281.52,
   "text": "In January, we can picture it closed and dark, its long porches empty,",
   "scene": 2
  },
  {
   "start": 281.52,
   "end": 284.13,
   "text": "its rooms waiting for summer.",
   "scene": 2
  },
  {
   "start": 288.13,
   "end": 294.91,
   "text": "There is a book of instructions for every keeper in the Light-House Service.",
   "scene": 3
  },
  {
   "start": 294.91,
   "end": 300.13,
   "text": "It is small and plain, and it is very clear.",
   "scene": 3
  },
  {
   "start": 302.13,
   "end": 307.35,
   "text": "It says that lights must be lighted punctually at sunset,",
   "scene": 3
  },
  {
   "start": 307.35,
   "end": 312.57,
   "text": "and must be kept burning at full intensity until sunrise.",
   "scene": 3
  },
  {
   "start": 315.57,
   "end": 320.78,
   "text": "It also says that all preparations must be made early,",
   "scene": 3
  },
  {
   "start": 320.78,
   "end": 325.48,
   "text": "so that there may be no delay in lighting.",
   "scene": 3
  },
  {
   "start": 328.48,
   "end": 331.61,
   "text": "That is why the afternoon matters.",
   "scene": 3
  },
  {
   "start": 331.61,
   "end": 337.35,
   "text": "Most of the work of a lighthouse is done in daylight,",
   "scene": 3
  },
  {
   "start": 337.35,
   "end": 342.04,
   "text": "so that the moment of lighting can be calm.",
   "scene": 3
  },
  {
   "start": 345.04,
   "end": 351.3,
   "text": "Today the sun sets at twenty-three minutes past four, by standard time.",
   "scene": 3
  },
  {
   "start": 351.3,
   "end": 357.57,
   "text": "Half an hour later, the last of the twilight will be gone.",
   "scene": 3
  },
  {
   "start": 359.57,
   "end": 363.74,
   "text": "You do not need to watch the clock.",
   "scene": 3
  },
  {
   "start": 363.74,
   "end": 367.39,
   "text": "You will see it in the sky.",
   "scene": 3
  },
  {
   "start": 367.39,
   "end": 371.57,
   "text": "The water darkens first. Then the far shore.",
   "scene": 3
  },
  {
   "start": 371.57,
   "end": 375.22,
   "text": "Then the sky, slowly, from the east.",
   "scene": 3
  },
  {
   "start": 379.22,
   "end": 382.87,
   "text": "Who keeps a light like this one?",
   "scene": 4
  },
  {
   "start": 384.87,
   "end": 390.61,
   "text": "The Light-House Board wrote that at stations needing only one keeper,",
   "scene": 4
  },
  {
   "start": 390.61,
   "end": 396.35,
   "text": "it often chose retired sea captains or mates who had families.",
   "scene": 4
  },
  {
   "start": 398.35,
   "end": 402.52,
   "text": "So perhaps you have been to sea yourself.",
   "scene": 4
  },
  {
   "start": 402.52,
   "end": 412.43,
   "text": "Perhaps you know, from the other side, what it means to see a steady light on a dark shore.",
   "scene": 4
  },
  {
   "start": 415.43,
   "end": 423.78,
   "text": "The Board also encouraged its keepers to work small farms or gardens, where the land allowed.",
   "scene": 4
  },
  {
   "start": 423.78,
   "end": 429.52,
   "text": "In January, whatever garden there is lies asleep under the cold.",
   "scene": 4
  },
  {
   "start": 432.52,
   "end": 441.39,
   "text": "And the pay for this station, in the government register for this year, is five hundred dollars.",
   "scene": 4
  },
  {
   "start": 445.39,
   "end": 449.57,
   "text": "The lamp is not in the tower yet.",
   "scene": 5
  },
  {
   "start": 449.57,
   "end": 453.22,
   "text": "It is here in the house, waiting.",
   "scene": 5
  },
  {
   "start": 455.22,
   "end": 459.91,
   "text": "The book has a rule for very cold weather.",
   "scene": 5
  },
  {
   "start": 459.91,
   "end": 465.13,
   "text": "When the lamp is filled and ready for the evening,",
   "scene": 5
  },
  {
   "start": 465.13,
   "end": 474.0,
   "text": "it should be kept in a room of moderate temperature, so that the oil does not chill.",
   "scene": 5
  },
  {
   "start": 477.0,
   "end": 486.39,
   "text": "So tonight the lamp sits somewhere warm, not too close to the stove, not too far from it.",
   "scene": 5
  },
  {
   "start": 486.39,
   "end": 495.78,
   "text": "Let us say it sits on the kitchen table, its brass catching a little of the window light.",
   "scene": 5
  },
  {
   "start": 498.78,
   "end": 502.43,
   "text": "It was filled earlier in the day.",
   "scene": 5
  },
  {
   "start": 502.43,
   "end": 509.22,
   "text": "The rule says to fill it nearly, but not quite, to the top.",
   "scene": 5
  },
  {
   "start": 509.22,
   "end": 516.0,
   "text": "A little room is left, because the oil grows larger as it warms.",
   "scene": 5
  },
  {
   "start": 519.0,
   "end": 525.26,
   "text": "You can rest your hand near it and feel nothing at all.",
   "scene": 5
  },
  {
   "start": 525.26,
   "end": 528.91,
   "text": "Cold brass. Still oil. A wick waiting.",
   "scene": 5
  },
  {
   "start": 532.91,
   "end": 536.04,
   "text": "The lamp burns mineral oil. Kerosene.",
   "scene": 6
  },
  {
   "start": 536.04,
   "end": 540.74,
   "text": "By now it is used throughout the lighthouse service.",
   "scene": 6
  },
  {
   "start": 542.74,
   "end": 550.57,
   "text": "A book from the Light-House Board, printed in eighteen eighty-nine, compares it with lard oil.",
   "scene": 6
  },
  {
   "start": 550.57,
   "end": 559.43,
   "text": "Five gallons of mineral oil, it says, give as much light as four gallons of lard oil,",
   "scene": 6
  },
  {
   "start": 559.43,
   "end": 561.52,
   "text": "and cost far less.",
   "scene": 6
  },
  {
   "start": 564.52,
   "end": 569.74,
   "text": "The Board set tests for the oil it would accept.",
   "scene": 6
  },
  {
   "start": 569.74,
   "end": 576.52,
   "text": "It had to pass a flash test at one hundred and forty degrees,",
   "scene": 6
  },
  {
   "start": 576.52,
   "end": 580.7,
   "text": "and stay clear and liquid even at zero.",
   "scene": 6
  },
  {
   "start": 583.7,
   "end": 589.43,
   "text": "There are rules about oil, and you keep them without thinking.",
   "scene": 6
  },
  {
   "start": 589.43,
   "end": 593.61,
   "text": "The oil must be drawn only by daylight.",
   "scene": 6
  },
  {
   "start": 593.61,
   "end": 598.3,
   "text": "Under no circumstances should it be drawn at night.",
   "scene": 6
  },
  {
   "start": 600.3,
   "end": 607.09,
   "text": "The cans are kept tightly closed, and the oil room cool and aired.",
   "scene": 6
  },
  {
   "start": 607.09,
   "end": 613.35,
   "text": "No one smokes there, and no uncovered light is ever taken there.",
   "scene": 6
  },
  {
   "start": 615.35,
   "end": 624.74,
   "text": "And oil is never, ever poured into a lamp while it is lit, or anywhere near a flame.",
   "scene": 6
  },
  {
   "start": 627.74,
   "end": 632.96,
   "text": "There is no separate oil house at this station yet.",
   "scene": 6
  },
  {
   "start": 632.96,
   "end": 635.57,
   "text": "That will come years later.",
   "scene": 6
  },
  {
   "start": 635.57,
   "end": 643.91,
   "text": "So for now, we imagine the cans stored somewhere cool and safe, away from the stove.",
   "scene": 6
  },
  {
   "start": 647.91,
   "end": 651.57,
   "text": "By the workroom door hangs your coat.",
   "scene": 7
  },
  {
   "start": 651.57,
   "end": 658.35,
   "text": "The service asks its keepers to wear the prescribed uniform at all times.",
   "scene": 7
  },
  {
   "start": 660.35,
   "end": 662.96,
   "text": "The cloth is dark blue.",
   "scene": 7
  },
  {
   "start": 662.96,
   "end": 669.74,
   "text": "The cap carries a small badge of yellow metal, shaped like a lighthouse.",
   "scene": 7
  },
  {
   "start": 672.74,
   "end": 674.83,
   "text": "There are two exceptions.",
   "scene": 7
  },
  {
   "start": 674.83,
   "end": 679.52,
   "text": "For outdoor work there is a brown working suit.",
   "scene": 7
  },
  {
   "start": 679.52,
   "end": 687.87,
   "text": "And when you clean the lens, the coat comes off, and a linen apron goes on.",
   "scene": 7
  },
  {
   "start": 689.87,
   "end": 693.52,
   "text": "The apron is not for your sake.",
   "scene": 7
  },
  {
   "start": 693.52,
   "end": 696.13,
   "text": "It is for the glass.",
   "scene": 7
  },
  {
   "start": 696.13,
   "end": 701.35,
   "text": "Rough wool could scratch the lens, and linen will not.",
   "scene": 7
  },
  {
   "start": 704.35,
   "end": 707.48,
   "text": "This morning, you wore that apron.",
   "scene": 7
  },
  {
   "start": 707.48,
   "end": 715.3,
   "text": "You cleaned the lens and the glass of the lantern, as you do every day.",
   "scene": 7
  },
  {
   "start": 717.3,
   "end": 723.04,
   "text": "First the feather brush, to lift away every grain of dust.",
   "scene": 7
  },
  {
   "start": 723.04,
   "end": 725.65,
   "text": "Then a soft linen cloth.",
   "scene": 7
  },
  {
   "start": 725.65,
   "end": 729.83,
   "text": "And last of all, the buff-skin, to polish.",
   "scene": 7
  },
  {
   "start": 732.83,
   "end": 742.22,
   "text": "The book warns that a skin which has been wet must never be used, because it will scratch.",
   "scene": 7
  },
  {
   "start": 742.22,
   "end": 747.43,
   "text": "So the buff-skin is kept dry, folded, in its place.",
   "scene": 7
  },
  {
   "start": 751.43,
   "end": 753.52,
   "text": "It is nearly time.",
   "scene": 8
  },
  {
   "start": 755.52,
   "end": 759.7,
   "text": "You put on your coat and your cap.",
   "scene": 8
  },
  {
   "start": 759.7,
   "end": 765.43,
   "text": "You take the lamp from the table, carefully, with both hands.",
   "scene": 8
  },
  {
   "start": 765.43,
   "end": 768.57,
   "text": "It is heavier than it looks.",
   "scene": 8
  },
  {
   "start": 771.57,
   "end": 775.22,
   "text": "You walk through the narrow brick workroom.",
   "scene": 8
  },
  {
   "start": 775.22,
   "end": 777.83,
   "text": "Your footsteps sound different here.",
   "scene": 8
  },
  {
   "start": 777.83,
   "end": 779.91,
   "text": "The walls are close.",
   "scene": 8
  },
  {
   "start": 779.91,
   "end": 786.7,
   "text": "The air is a little colder with every step away from the kitchen.",
   "scene": 8
  },
  {
   "start": 789.7,
   "end": 794.91,
   "text": "At the foot of the tower, you begin to climb.",
   "scene": 8
  },
  {
   "start": 794.91,
   "end": 799.09,
   "text": "The stairs turn upward in the half dark.",
   "scene": 8
  },
  {
   "start": 799.09,
   "end": 803.26,
   "text": "You do not need a light for them.",
   "scene": 8
  },
  {
   "start": 803.26,
   "end": 805.35,
   "text": "You know every step.",
   "scene": 8
  },
  {
   "start": 809.35,
   "end": 815.61,
   "text": "As you climb, the sounds of the house fall away below you.",
   "scene": 8
  },
  {
   "start": 815.61,
   "end": 823.43,
   "text": "Soon there is only your breath, and the stairs, and the wind against the brick.",
   "scene": 8
  },
  {
   "start": 827.43,
   "end": 832.13,
   "text": "At the top, you step up into the lantern.",
   "scene": 9
  },
  {
   "start": 834.13,
   "end": 840.39,
   "text": "All day, linen curtains have hung around the inside of the glass.",
   "scene": 9
  },
  {
   "start": 840.39,
   "end": 847.17,
   "text": "You hung them this morning, when you put out the light at sunrise.",
   "scene": 9
  },
  {
   "start": 850.17,
   "end": 852.26,
   "text": "The reason is simple.",
   "scene": 9
  },
  {
   "start": 852.26,
   "end": 861.65,
   "text": "A lens that can throw a light sixteen nautical miles across the water can also gather the sun.",
   "scene": 9
  },
  {
   "start": 861.65,
   "end": 868.96,
   "text": "Left uncovered on a bright day, it could focus the sunlight and do harm,",
   "scene": 9
  },
  {
   "start": 868.96,
   "end": 873.13,
   "text": "and the glass could slowly change its color.",
   "scene": 9
  },
  {
   "start": 876.13,
   "end": 879.78,
   "text": "Now, at dusk, the curtains come down.",
   "scene": 9
  },
  {
   "start": 879.78,
   "end": 883.43,
   "text": "Keepers took them down in the evening,",
   "scene": 9
  },
  {
   "start": 883.43,
   "end": 889.17,
   "text": "so that nothing would stand between the lamp and the water.",
   "scene": 9
  },
  {
   "start": 892.17,
   "end": 897.91,
   "text": "You fold them, one at a time. The linen is cold.",
   "scene": 9
  },
  {
   "start": 897.91,
   "end": 902.09,
   "text": "The light behind it is grey and blue.",
   "scene": 9
  },
  {
   "start": 905.09,
   "end": 907.7,
   "text": "There is another rule here.",
   "scene": 9
  },
  {
   "start": 907.7,
   "end": 910.3,
   "text": "While the light is burning,",
   "scene": 9
  },
  {
   "start": 910.3,
   "end": 917.09,
   "text": "everything which does not belong in the lantern must be removed from it.",
   "scene": 9
  },
  {
   "start": 919.09,
   "end": 926.39,
   "text": "So you carry the curtains down a few steps, and leave them there, folded.",
   "scene": 9
  },
  {
   "start": 926.39,
   "end": 931.09,
   "text": "The lantern holds only what it needs. The lens.",
   "scene": 9
  },
  {
   "start": 931.09,
   "end": 933.17,
   "text": "The lamp. And you.",
   "scene": 9
  },
  {
   "start": 937.17,
   "end": 946.57,
   "text": "Let us look at the lens for a moment, while there is still a little daylight in it.",
   "scene": 10
  },
  {
   "start": 948.57,
   "end": 953.26,
   "text": "It is a Fresnel lens, of the fourth order.",
   "scene": 10
  },
  {
   "start": 953.26,
   "end": 960.04,
   "text": "The orders are sizes, and the fourth is one of the smaller ones.",
   "scene": 10
  },
  {
   "start": 963.04,
   "end": 971.39,
   "text": "It is built of rings of glass prisms, one above another, held in a metal frame.",
   "scene": 10
  },
  {
   "start": 971.39,
   "end": 977.13,
   "text": "The prisms bend and reflect the light of one small flame,",
   "scene": 10
  },
  {
   "start": 977.13,
   "end": 984.43,
   "text": "rays that would scatter in every direction, and send them out toward the water.",
   "scene": 10
  },
  {
   "start": 987.43,
   "end": 993.7,
   "text": "At this station, the light does not turn and does not flash.",
   "scene": 10
  },
  {
   "start": 993.7,
   "end": 996.83,
   "text": "It is a fixed white light.",
   "scene": 10
  },
  {
   "start": 996.83,
   "end": 999.96,
   "text": "It simply shines, steady, all night.",
   "scene": 10
  },
  {
   "start": 1002.96,
   "end": 1011.3,
   "text": "A ship coming up the bay will see it as a single, still point of white,",
   "scene": 10
  },
  {
   "start": 1011.3,
   "end": 1014.43,
   "text": "marking the way into the river.",
   "scene": 10
  },
  {
   "start": 1018.43,
   "end": 1021.04,
   "text": "The sun is down now.",
   "scene": 11
  },
  {
   "start": 1021.04,
   "end": 1029.91,
   "text": "The water has gone dark, and the sky over the far shore is the color of ashes.",
   "scene": 11
  },
  {
   "start": 1032.91,
   "end": 1041.78,
   "text": "The book says the lamp must be placed inside the lens, in its place, and then lighted.",
   "scene": 11
  },
  {
   "start": 1043.78,
   "end": 1051.09,
   "text": "So you set it down, gently, at the very center of all that glass.",
   "scene": 11
  },
  {
   "start": 1054.09,
   "end": 1058.78,
   "text": "You strike a match. The wick takes the flame.",
   "scene": 11
  },
  {
   "start": 1062.78,
   "end": 1067.48,
   "text": "And now comes the part that cannot be hurried.",
   "scene": 11
  },
  {
   "start": 1069.48,
   "end": 1075.22,
   "text": "For the first half hour, the flame must be kept low.",
   "scene": 11
  },
  {
   "start": 1075.22,
   "end": 1080.43,
   "text": "The glass chimney of the lamp has to warm slowly.",
   "scene": 11
  },
  {
   "start": 1080.43,
   "end": 1088.78,
   "text": "If you turn the wick up too soon, before the chimney and the burner are warm,",
   "scene": 11
  },
  {
   "start": 1088.78,
   "end": 1090.87,
   "text": "the lamp will smoke.",
   "scene": 11
  },
  {
   "start": 1094.87,
   "end": 1097.48,
   "text": "So you keep it low.",
   "scene": 11
  },
  {
   "start": 1097.48,
   "end": 1102.7,
   "text": "A small flame, in the middle of the great glass.",
   "scene": 11
  },
  {
   "start": 1105.7,
   "end": 1109.35,
   "text": "And slowly, the lens begins to fill.",
   "scene": 11
  },
  {
   "start": 1109.35,
   "end": 1116.13,
   "text": "Ring after ring takes the light, until the whole lantern glows with it.",
   "scene": 11
  },
  {
   "start": 1121.13,
   "end": 1126.87,
   "text": "From the gallery outside, if you stepped out into the cold,",
   "scene": 12
  },
  {
   "start": 1126.87,
   "end": 1135.22,
   "text": "you would see the light laid out over the water, low and level, toward the ships.",
   "scene": 12
  },
  {
   "start": 1138.22,
   "end": 1144.48,
   "text": "It will burn now until sunrise, at full strength, without a break.",
   "scene": 12
  },
  {
   "start": 1147.48,
   "end": 1153.74,
   "text": "The Weather Bureau's map for this evening shows clearing weather moving east,",
   "scene": 12
  },
  {
   "start": 1153.74,
   "end": 1159.48,
   "text": "toward New England, and the forecast for tomorrow is generally fair.",
   "scene": 12
  },
  {
   "start": 1159.48,
   "end": 1162.61,
   "text": "At Eastport, further along the coast,",
   "scene": 12
  },
  {
   "start": 1162.61,
   "end": 1168.35,
   "text": "the thermometer will read ten degrees above zero at eight o'clock.",
   "scene": 12
  },
  {
   "start": 1170.35,
   "end": 1177.65,
   "text": "Here at the point, we can imagine the same: a cold, still, clear night.",
   "scene": 12
  },
  {
   "start": 1180.65,
   "end": 1184.83,
   "text": "The stars are coming out over the bay.",
   "scene": 12
  },
  {
   "start": 1184.83,
   "end": 1194.22,
   "text": "And in about two and a half hours, a moon just past full will rise in the east,",
   "scene": 12
  },
  {
   "start": 1194.22,
   "end": 1198.91,
   "text": "and lay its own pale road across the water.",
   "scene": 12
  },
  {
   "start": 1202.91,
   "end": 1210.22,
   "text": "The list of lights for these years gives no winter pause for this station.",
   "scene": 12
  },
  {
   "start": 1210.22,
   "end": 1221.17,
   "text": "The rules say a light must always be shown if it is at all possible for vessels to benefit by it.",
   "scene": 12
  },
  {
   "start": 1225.17,
   "end": 1227.26,
   "text": "The lamp is lit.",
   "scene": 13
  },
  {
   "start": 1227.26,
   "end": 1231.96,
   "text": "The hardest part of the evening is already done.",
   "scene": 13
  },
  {
   "start": 1234.96,
   "end": 1242.26,
   "text": "The government register for this year lists one name at this station, the keeper's.",
   "scene": 13
  },
  {
   "start": 1242.26,
   "end": 1244.35,
   "text": "No assistant is listed.",
   "scene": 13
  },
  {
   "start": 1246.35,
   "end": 1255.74,
   "text": "For a keeper alone, the book says, the light must be visited at least twice during the night,",
   "scene": 13
  },
  {
   "start": 1255.74,
   "end": 1258.35,
   "text": "between eight o'clock and sunrise.",
   "scene": 13
  },
  {
   "start": 1258.35,
   "end": 1263.57,
   "text": "And on stormy nights, it must be constantly looked after.",
   "scene": 13
  },
  {
   "start": 1266.57,
   "end": 1269.7,
   "text": "Tonight is not a stormy night.",
   "scene": 13
  },
  {
   "start": 1269.7,
   "end": 1275.96,
   "text": "So you will climb these stairs twice more, in the dark hours.",
   "scene": 13
  },
  {
   "start": 1275.96,
   "end": 1277.52,
   "text": "That is all.",
   "scene": 13
  },
  {
   "start": 1280.52,
   "end": 1284.7,
   "text": "The station must never be left wholly unattended.",
   "scene": 13
  },
  {
   "start": 1284.7,
   "end": 1293.57,
   "text": "If a keeper must be away, a member of his family, or another responsible person, must stay.",
   "scene": 13
  },
  {
   "start": 1296.57,
   "end": 1300.74,
   "text": "Later this evening, you will open the journal.",
   "scene": 13
  },
  {
   "start": 1300.74,
   "end": 1307.0,
   "text": "Each day takes one line, written across both pages, in ink, neatly.",
   "scene": 13
  },
  {
   "start": 1307.0,
   "end": 1313.26,
   "text": "The weather goes in it, and anything of interest on the water.",
   "scene": 13
  },
  {
   "start": 1316.26,
   "end": 1321.48,
   "text": "One line for a whole day. It seems very little.",
   "scene": 13
  },
  {
   "start": 1321.48,
   "end": 1326.17,
   "text": "But on a quiet day, one line is enough.",
   "scene": 13
  },
  {
   "start": 1329.17,
   "end": 1330.74,
   "text": "Tomorrow is Sunday.",
   "scene": 13
  },
  {
   "start": 1330.74,
   "end": 1337.52,
   "text": "The rules allow a keeper to be away on Sundays to attend church,",
   "scene": 13
  },
  {
   "start": 1337.52,
   "end": 1344.3,
   "text": "so long as the light is never left without someone to watch it.",
   "scene": 13
  },
  {
   "start": 1347.3,
   "end": 1349.39,
   "text": "But that is tomorrow.",
   "scene": 13
  },
  {
   "start": 1349.39,
   "end": 1352.0,
   "text": "Tonight there is only tonight.",
   "scene": 13
  },
  {
   "start": 1356.0,
   "end": 1360.7,
   "text": "So the first part of the night is done.",
   "scene": 14
  },
  {
   "start": 1363.7,
   "end": 1368.91,
   "text": "The lamp is burning low and steady, warming its glass.",
   "scene": 14
  },
  {
   "start": 1368.91,
   "end": 1371.52,
   "text": "The kitchen is warm below.",
   "scene": 14
  },
  {
   "start": 1371.52,
   "end": 1374.65,
   "text": "The bay is dark and calm.",
   "scene": 14
  },
  {
   "start": 1377.65,
   "end": 1381.83,
   "text": "There is nothing you need to do now.",
   "scene": 14
  },
  {
   "start": 1381.83,
   "end": 1384.43,
   "text": "Nothing you need to remember.",
   "scene": 14
  },
  {
   "start": 1387.43,
   "end": 1395.26,
   "text": "Just the light above you, keeping its watch, so that you do not have to.",
   "scene": 14
  },
  {
   "start": 1400.26,
   "end": 1401.3,
   "text": "Rest now.",
   "scene": 14
  }
 ]
}
~~~~

### `src/index.ts`

~~~~ts
import {registerRoot} from 'remotion';
import {RemotionRoot} from './Root';

registerRoot(RemotionRoot);
~~~~

### `src/palette.ts`

~~~~ts
// Channel palette from docs/channel-concepts/lantern-library/concept.md ("Оформление варианта A").
export const P = {
	night: '#0f1426',
	dusk: '#1d2340',
	steel: '#3b4a5e',
	plaster: '#e9d9bd',
	amber: '#f2b45a', // fire and lamps only
	coal: '#c4573a',
	snow: '#cdd3df',
	iron: '#131826',
};
~~~~

### `tools/ambience.py`

~~~~python
"""Sea and wind for the 30-second probe, made from filtered noise. No recordings.

Usage: python3 -I tools/ambience.py public/ambience.wav
Seeded: the same file comes out every run.
"""
import sys
import wave

import numpy as np

SR = 48000
DUR = 30.0
N = int(SR * DUR)
rng = np.random.default_rng(1891)
t = np.arange(N) / SR


def shaped_noise(curve, seed):
    """White noise shaped in the frequency domain by curve(freqs)."""
    r = np.random.default_rng(seed)
    spec = np.fft.rfft(r.standard_normal(N))
    freqs = np.fft.rfftfreq(N, 1 / SR)
    out = np.fft.irfft(spec * curve(freqs), N)
    return out / np.max(np.abs(out))


def smooth(x, sec):
    k = max(1, int(sec * SR))
    c = np.cumsum(np.insert(x, 0, 0.0))
    y = (c[k:] - c[:-k]) / k
    return np.concatenate([y, np.full(k - 1, y[-1])])


def lowpass(f, fc, order=2):
    return 1 / np.sqrt(1 + (f / fc) ** (2 * order))


def highpass(f, fc, order=2):
    return 1 / np.sqrt(1 + (fc / np.maximum(f, 1e-3)) ** (2 * order))


# sea: rumble under everything, waves that rise and wash back, foam hiss on the wash
rumble = lambda f: highpass(f, 35) * lowpass(f, 380, 2) / np.sqrt(np.maximum(f, 20) / 20)
foam = lambda f: highpass(f, 1800, 2) * lowpass(f, 7000, 2)
swell = np.zeros(N)
foam_env = np.zeros(N)
start = 0.8
while start < DUR:
    rise, fall = 2.2 + rng.random(), 3.5 + 1.5 * rng.random()
    a = 0.6 + 0.4 * rng.random()
    x = t - start
    env = np.where(x < 0, 0, np.where(x < rise, (x / rise) ** 2, np.exp(-(x - rise) / fall)))
    swell += a * env
    foam_env += a * np.where(x < rise, 0, np.exp(-(x - rise) / (fall * 0.6))) * np.clip(x - rise, 0, 0.4) / 0.4
    start += 6.0 + 3.0 * rng.random()

sea = {}
for ch, seed in (('L', 11), ('R', 12)):
    shared = shaped_noise(rumble, 10)
    own = shaped_noise(rumble, seed)
    body = 0.75 * shared + 0.25 * own
    hiss = shaped_noise(foam, seed + 20)
    sea[ch] = body * (0.35 + 0.65 * swell) + 0.22 * hiss * foam_env

# wind: a band of noise whose level breathes slowly
wind_band = lambda f: highpass(f, 300, 2) * lowpass(f, 1100, 2)
gust = smooth(rng.standard_normal(N), 1.5)
gust = 0.55 + 0.45 * (gust - gust.min()) / (gust.max() - gust.min())
wind = {ch: shaped_noise(wind_band, seed) * gust for ch, seed in (('L', 31), ('R', 32))}

# inside the tower (about 18-26 s): the outside goes dull and quieter
inside = np.clip((t - 17.5) / 1.5, 0, 1) * np.clip((26.5 - t) / 1.5, 0, 1)
muffle = lambda f: lowpass(f, 420, 2)

mix = {}
for ch in ('L', 'R'):
    open_air = 0.8 * sea[ch] + 0.18 * wind[ch]
    spec = np.fft.rfft(open_air)
    dull = np.fft.irfft(spec * muffle(np.fft.rfftfreq(N, 1 / SR)), N)
    mix[ch] = open_air * (1 - inside) + 0.55 * dull * inside

fade = np.clip((t - 1.5) / 2.5, 0, 1) * np.clip((DUR - t) / 2.5, 0, 1)
stereo = np.stack([mix['L'] * fade, mix['R'] * fade], axis=1)
stereo *= 10 ** (-14 / 20) / np.max(np.abs(stereo))  # peak at -14 dBFS: calm and even

with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((stereo * 32767).astype('<i2').tobytes())
rms = 20 * np.log10(np.sqrt(np.mean(stereo[int(4 * SR):int(27 * SR)] ** 2)))
print(f'wrote {sys.argv[1]}: {DUR:.0f} s, RMS {rms:.1f} dBFS')
~~~~

### `tools/ambience_chapter.py`

~~~~python
"""Sea and wind for a whole chapter, from filtered noise, made in blocks. No recordings.

Same sound as tools/ambience.py, built block by block so a 25-minute chapter
fits in memory. Indoors (from the timeline) the outside goes dull and quieter.
The level falls slowly through the chapter, as the evening settles.

usage: python3 -I tools/ambience_chapter.py src/chapter1.json public/chapter1-ambience.wav
Seeded: the same file comes out every run.
"""
import json
import sys
import wave

import numpy as np

SR = 48000
BLOCK = 20.0
XF = 2.0  # crossfade between blocks, seconds

tl = json.load(open(sys.argv[1]))
DUR = tl['duration']
S = tl['scenes']


def cue(text):
    return next(c['start'] for c in tl['cues'] if text in c['text'])


# indoors: kitchen to lantern (scenes 5-11), and the journal in scene 13
INSIDE = [(S[4]['start'], S[11]['start'] + 4), (cue('Later this evening, you will open'), cue('Tomorrow is Sunday'))]

rng = np.random.default_rng(1892)
# wave events and slow gusts on the whole timeline
events = []
t0 = 0.8
while t0 < DUR + 10:
    events.append((t0, 2.2 + rng.random(), 3.5 + 1.5 * rng.random(), 0.6 + 0.4 * rng.random()))
    t0 += 6.0 + 3.0 * rng.random()
gust_parts = [(rng.random() * 2 * np.pi, 1 / (4 + 10 * rng.random())) for _ in range(6)]


def lowpass(f, fc, order=2):
    return 1 / np.sqrt(1 + (f / fc) ** (2 * order))


def highpass(f, fc, order=2):
    return 1 / np.sqrt(1 + (fc / np.maximum(f, 1e-3)) ** (2 * order))


rumble = lambda f: highpass(f, 35) * lowpass(f, 380, 2) / np.sqrt(np.maximum(f, 20) / 20)
foam = lambda f: highpass(f, 1800, 2) * lowpass(f, 7000, 2)
wind_band = lambda f: highpass(f, 300, 2) * lowpass(f, 1100, 2)
muffle = lambda f: lowpass(f, 420, 2)


def block(start, n, seed):
    t = start + np.arange(n) / SR
    freqs = np.fft.rfftfreq(n, 1 / SR)

    def noise(curve, s):
        spec = np.fft.rfft(np.random.default_rng(seed * 100 + s).standard_normal(n))
        x = np.fft.irfft(spec * curve(freqs), n)
        return x / np.sqrt(np.mean(x ** 2)) / 4.8  # as the probe's peak-normalised noise

    swell = np.zeros(n)
    foam_env = np.zeros(n)
    for (e, rise, fall, a) in events:
        if e > t[-1] or e + rise + 8 * fall < t[0]:
            continue
        x = t - e
        swell += a * np.where(x < 0, 0, np.where(x < rise, (x / rise) ** 2, np.exp(-(x - rise) / fall)))
        foam_env += a * np.where(x < rise, 0, np.exp(-(x - rise) / (fall * 0.6))) * np.clip(x - rise, 0, 0.4) / 0.4
    gust = sum(np.sin(2 * np.pi * fr * t + ph) for ph, fr in gust_parts) / len(gust_parts)
    gust = 0.55 + 0.45 * (gust + 1) / 2
    inside = np.zeros(n)
    for a, b in INSIDE:
        inside = np.maximum(inside, np.clip((t - a) / 2, 0, 1) * np.clip((b - t) / 2, 0, 1))
    shared = noise(rumble, 0)
    out = []
    for ch in (1, 2):
        body = 0.75 * shared + 0.25 * noise(rumble, ch)
        sea = body * (0.35 + 0.65 * swell) + 0.22 * noise(foam, 10 + ch) * foam_env
        wind = noise(wind_band, 20 + ch) * gust
        open_air = 0.8 * sea + 0.18 * wind
        dull = np.fft.irfft(np.fft.rfft(open_air) * muffle(freqs), n)
        out.append(open_air * (1 - inside) + 0.55 * dull * inside)
    return np.stack(out, axis=1)


n_total = int(DUR * SR)
step = int(BLOCK * SR)
xf = int(XF * SR)
mix = np.zeros((n_total, 2), dtype=np.float32)
pos, i = 0, 0
while pos < n_total:
    n = min(step + xf, n_total - pos)
    b = block(pos / SR, n, i + 1)
    w = np.ones(n)
    if pos > 0:
        w[:xf] = np.sin(np.linspace(0, np.pi / 2, xf)) ** 2
    if pos + n < n_total:
        w[-xf:] = np.cos(np.linspace(0, np.pi / 2, xf)) ** 2
    mix[pos:pos + n] += (b * w[:, None]).astype(np.float32)
    pos += step
    i += 1

# level and fades, applied in chunks to keep memory low
CH = SR * 60
for p0 in range(0, n_total, CH):
    t = (p0 + np.arange(min(CH, n_total - p0))) / SR
    level = 10 ** (np.interp(t, [0, DUR], [0, -4]) / 20)  # evening settles: 4 dB quieter by the end
    fade = np.clip((t - 1.5) / 3.0, 0, 1) * np.clip((DUR - t) / 6.0, 0, 1)
    mix[p0:p0 + len(t)] *= (level * fade)[:, None].astype(np.float32)
# the same calm level as the probe: RMS of the first open-air minute at about -30 dBFS
ref = mix[int(5 * SR):int(65 * SR)]
mix *= np.float32(10 ** (-30 / 20) / np.sqrt(np.mean(ref.astype(np.float64) ** 2)))
peak = float(np.max(np.abs(mix)))
if peak > 10 ** (-12 / 20):
    mix *= np.float32(10 ** (-12 / 20) / peak)

with wave.open(sys.argv[2], 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    for p0 in range(0, n_total, CH):
        w.writeframes((mix[p0:p0 + CH] * 32767).astype('<i2').tobytes())
print(f'wrote {sys.argv[2]}: {DUR / 60:.2f} min, peak {20 * np.log10(np.max(np.abs(mix))):.1f} dBFS')
~~~~

### `tools/check.py`

~~~~python
"""Measurable quality checks for a rendered video: frames, brightness, flashes, loudness.

Usage (from the probe folder): python3 -I tools/check.py out/lighthouse-probe.mp4
Uses the FFmpeg that ships with Remotion (`bunx remotion ffmpeg`).
"""
import json
import subprocess
import sys

import numpy as np

path = sys.argv[1]
FW, FH = 160, 90


def ffmpeg(*args, capture='stdout', tool='ffmpeg'):
    r = subprocess.run(['bunx', 'remotion', tool, '-hide_banner', *args], capture_output=True)
    if r.returncode != 0:
        sys.exit(r.stderr.decode()[-2000:])
    return r.stdout if capture == 'stdout' else r.stderr.decode()


info = ffmpeg('-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate', '-of', 'csv=p=0', path, tool='ffprobe')
num, den = info.decode().strip().strip(',').split('/')
fps = float(num) / float(den)
# frames are read in a stream: a 25-minute chapter does not fit in memory at once
proc = subprocess.Popen(['bunx', 'remotion', 'ffmpeg', '-hide_banner', '-v', 'error', '-i', path, '-vf', f'scale={FW}:{FH}',
    '-pix_fmt', 'gray', '-c:v', 'rawvideo', '-f', 'image2pipe', '-'], stdout=subprocess.PIPE)
luma = []
size = FW * FH
while True:
    buf = proc.stdout.read(size * 300)
    if not buf:
        break
    n = len(buf) // size
    luma.extend(np.frombuffer(buf[:n * size], np.uint8).reshape(n, size).mean(axis=1) / 255 * 100)
proc.wait()
luma = np.array(luma)
delta = np.abs(np.diff(luma))
step = int(fps) if len(luma) < 120 * fps else int(fps * 60)
unit = 'second' if step == int(fps) else 'minute'
per = [luma[i:i + step].mean() for i in range(0, len(luma), step)]

loud = ffmpeg('-i', path, '-vn', '-af', 'loudnorm=I=-20:TP=-2:LRA=7:print_format=json', '-c:a', 'pcm_s16le', '-f', 'wav', '-y', '/dev/null', capture='stderr')
stats = json.loads(loud[loud.rindex('{'):loud.rindex('}') + 1])

frames = luma
print(f'frames {len(frames)} at {fps:g} fps = {len(frames) / fps:.2f} s')
print(f'mean brightness per {unit}, % of white:', ' '.join(f'{v:.0f}' for v in per))
print(f'first minute {luma[:int(fps * 60)].mean():.1f}%, last minute {luma[-int(fps * 60):].mean():.1f}%')
print(f'largest frame-to-frame brightness jump: {delta.max():.2f} points at {delta.argmax() / fps:.2f} s')
print(f'frames with a jump over 2 points: {(delta > 2).sum()}')
print(f"loudness: integrated {stats['input_i']} LUFS, true peak {stats['input_tp']} dBTP, range {stats['input_lra']} LU")
~~~~

### `tools/grain.py`

~~~~python
"""Paper grain tile for the probe: 512x512 grey noise, seeded.

Usage: python3 -I sound/grain.py public/grain.png
"""
import sys

import numpy as np
from PIL import Image

rng = np.random.default_rng(1891)
n = rng.normal(128, 30, (512, 512))
Image.fromarray(np.clip(n, 0, 255).astype('uint8'), 'L').save(sys.argv[1], optimize=True)
~~~~

### `tools/mux_chapter.sh`

~~~~bash
#!/usr/bin/env bash
# Join the rendered segments without re-encoding and add the sound once.
# usage: tools/mux_chapter.sh out/ch1 out/chapter1.mp4            ambience only (silent cut)
#        tools/mux_chapter.sh out/ch1 out/chapter1.mp4 voice      voice + ambience 6 dB under it
set -euo pipefail
DIR=${1:?segment dir}
OUT=${2:?output file}
: > "$DIR/list.txt"
for f in "$DIR"/seg0[0-9].mp4; do echo "file '$(realpath "$f")'" >> "$DIR/list.txt"; done
if [ "${3:-}" = voice ]; then
  bunx remotion ffmpeg -hide_banner -v error -y -f concat -safe 0 -i "$DIR/list.txt" -i public/chapter1-ambience.wav -i public/chapter1-voice.wav \
    -filter_complex "[1:a]volume=0.5[amb];[amb][2:a]amix=inputs=2:normalize=0:duration=first[a]" \
    -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 384k -ar 48000 -shortest -movflags +faststart "$OUT"
else
  bunx remotion ffmpeg -hide_banner -v error -y -f concat -safe 0 -i "$DIR/list.txt" -i public/chapter1-ambience.wav \
    -map 0:v -map 1:a -c:v copy -c:a aac -b:a 384k -ar 48000 -shortest -movflags +faststart "$OUT"
fi
echo "wrote $OUT"
~~~~

### `tools/render_chapter.sh`

~~~~bash
#!/usr/bin/env bash
# Render chapter 1 in segments without sound, log wall time of each.
# usage: tools/render_chapter.sh out/ch1 [props-json]   (from the probe folder)
#   silent cut: default props; voiced pilot: '{"audio":false,"captions":false}'
set -euo pipefail
OUT=${1:?out dir}
PROPS=${2:-'{"audio":false}'}
mkdir -p "$OUT"
TOTAL=$(python3 -c "import json;print(round(json.load(open('src/chapter1.json'))['duration']*30))")
bunx remotion bundle src/index.ts --out-dir=out/bundle >/dev/null
starts=(0 5400 14400 23400 32400)
for i in "${!starts[@]}"; do
  a=${starts[$i]}
  if [ $((i + 1)) -lt ${#starts[@]} ]; then b=$((starts[$((i + 1))] - 1)); else b=$((TOTAL - 1)); fi
  seg=$(printf '%s/seg%02d.mp4' "$OUT" "$i")
  t0=$(date +%s)
  bunx remotion render out/bundle Chapter1 "$seg" --frames=$a-$b --codec=h264 --crf=18 --concurrency=3 --muted --props="$PROPS" >"$OUT/seg$i.log" 2>&1
  echo "seg$i frames $a-$b: $(( $(date +%s) - t0 )) s" | tee -a "$OUT/times.txt"
done
~~~~

### `tools/timeline.py`

~~~~python
"""Chapter timeline from the script: scenes, narration cues, subtitles.

Without a voice the timing is estimated: WPM words per minute plus the
script's pauses. With a voice the same cues get real times from the
ElevenLabs timestamps (not done yet).

usage: python3 tools/timeline.py ../script/chapter-1-dusk.md src/chapter1.json ../script/chapter-1-dusk.estimated.srt [voice/ch1]
With a voice folder (tools/voice.py chapter) every paragraph and cue takes its time from the voice.
"""
import json
import os
import re
import sys

WPM = 115
LEAD = 3.0   # silence before the first word
TAIL = 8.0   # after the last pause: the fade to black
MAX_CUE = 96  # characters per subtitle cue


def chunks(sentence):
    """Split a long sentence at commas or semicolons into cues of at most MAX_CUE characters."""
    if len(sentence) <= MAX_CUE:
        return [sentence]
    parts = re.split(r'(?<=[,;:])\s+', sentence)
    out, cur = [], ''
    for p in parts:
        if cur and len(cur) + 1 + len(p) > MAX_CUE:
            out.append(cur)
            cur = p
        else:
            cur = f'{cur} {p}'.strip()
    if cur:
        out.append(cur)
    return out


def cue_parts(v):
    """A paragraph as subtitle cues: short sentences joined, long ones split."""
    sentences = []
    for sen in re.split(r'(?<=[.!?])\s+', v):
        if sentences and len(sentences[-1]) + 1 + len(sen) <= 48:
            sentences[-1] += ' ' + sen
        else:
            sentences.append(sen)
    return [part for sen in sentences for part in chunks(sen)]


def parse(md):
    scenes, sec = [], None
    for line in open(md, encoding='utf-8'):
        line = line.strip()
        m = re.match(r'^## (\d+а?)\. (.+)$', line)
        if m:
            sec = {'id': m.group(1), 'title': m.group(2), 'items': []}
            scenes.append(sec)
            continue
        if line.startswith('## '):
            sec = None
            continue
        if not sec or not line or line.startswith('Пояснение') or line.startswith('[scene'):
            continue
        p = re.match(r'^\[pause (\d+(?:\.\d+)?)s\]$', line)
        if p:
            sec['items'].append(('pause', float(p.group(1))))
        elif not re.search('[а-яА-Я]', line):
            sec['items'].append(('text', re.sub(r'\s*\{[cr]\d+~?\}', '', line).strip()))
    return scenes


def voiced(voice_dir, n):
    """Alignment of paragraph n from the voice, or None."""
    path = os.path.join(voice_dir, f'p{n:03d}.mp3.json') if voice_dir else ''
    return json.load(open(path))['alignment'] if path and os.path.exists(path) else None


def build(md, voice_dir=None):
    scenes = parse(md)
    t = LEAD
    cues, out, voice = [], [], []
    n = 0
    for i, s in enumerate(scenes):
        start = t
        for kind, v in s['items']:
            if kind == 'pause':
                t += v
                continue
            n += 1
            al = voiced(voice_dir, n)
            if al:
                # real times: each cue spans its characters in the voice alignment
                st, en = al['character_start_times_seconds'], al['character_end_times_seconds']
                pos = 0
                for part in cue_parts(v):
                    a = v.find(part, pos)
                    b = a + len(part) - 1
                    pos = b + 1
                    cues.append({'start': round(t + st[a], 2), 'end': round(t + en[b], 2), 'text': part, 'scene': i + 1})
                voice.append({'start': round(t, 3), 'n': n})
                t += en[-1] + 0.2
                continue
            for part in cue_parts(v):
                d = len(part.split()) / WPM * 60
                cues.append({'start': round(t, 2), 'end': round(t + d, 2), 'text': part, 'scene': i + 1})
                t += d
        out.append({'n': i + 1, 'title': s['title'], 'start': round(start, 2), 'end': round(t, 2)})
    t += TAIL
    out[-1]['end'] = round(t, 2)
    return {'wpm': None if voice else WPM, 'duration': round(t, 2), 'scenes': out, 'cues': cues, 'voice': voice}


def srt_time(s):
    ms = int(round(s * 1000))
    return f'{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}'


if __name__ == '__main__':
    md, js, srt = sys.argv[1:4]
    tl = build(md, sys.argv[4] if len(sys.argv) > 4 else None)
    json.dump(tl, open(js, 'w'), indent=1, ensure_ascii=False)
    with open(srt, 'w', encoding='utf-8') as f:
        for i, c in enumerate(tl['cues'], 1):
            f.write(f"{i}\n{srt_time(c['start'])} --> {srt_time(c['end'])}\n{c['text']}\n\n")
    words = sum(len(c['text'].split()) for c in tl['cues'])
    print(f"{len(tl['scenes'])} scenes, {len(tl['cues'])} cues, {words} words, {tl['duration'] / 60:.2f} min")
    for s in tl['scenes']:
        print(f"{s['n']:2d} {s['start'] / 60:5.2f}-{s['end'] / 60:5.2f} {s['title']}")
~~~~

### `tools/voice.py`

~~~~python
"""ElevenLabs voice for chapter 1, through the board's spend route. PAID: run only with permission.

usage (from the probe folder):
  python3 -I tools/voice.py count                         characters per step, no calls
  python3 -I tools/voice.py casting A=VOICE_ID B=VOICE_ID   the casting excerpt in each voice -> voice/casting/A.mp3
  python3 -I tools/voice.py names VOICE_ID                 place names alone, to check pronunciation
  python3 -I tools/voice.py chapter VOICE_ID               every paragraph of chapter 1 -> voice/ch1/p001.mp3 + .json

Each result is cached by text, voice, model and settings: a second run of the same text costs nothing.
The first HTTP error stops the run (402 spend_cap included): no retries, no other route.
Every paid request is logged with its character count in voice/calls.log.
"""
import base64
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.error
from urllib.request import Request, urlopen

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timeline import parse  # noqa: E402

MODEL = 'eleven_multilingual_v2'
SETTINGS = {'stability': 0.6, 'similarity_boost': 0.75, 'style': 0.0, 'use_speaker_boost': True, 'speed': 0.88}
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(HERE, '..', 'script', 'chapter-1-dusk.md')
EXCERPT = os.path.join(HERE, '..', 'script', 'voice-casting-excerpt.txt')
NAMES = 'Fort Point. Stockton Springs. The Penobscot River. Cape Jellison. A Fresnel lens. Eastport, Maine.'
OUT = os.path.join(HERE, 'voice')

top = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True, cwd=HERE).stdout.strip()
SESSION = os.path.basename(top)
BASE = f'http://127.0.0.1:41806/spend/v1/{SESSION}/voice/elevenlabs'


def paragraphs():
    out = []
    for s in parse(SCRIPT):
        out += [v for kind, v in s['items'] if kind == 'text']
    return out


def synth(text, voice, path):
    key = hashlib.sha256(json.dumps([text, voice, MODEL, SETTINGS]).encode()).hexdigest()[:16]
    meta = path + '.json'
    if os.path.exists(meta) and json.load(open(meta)).get('key') == key:
        return 0
    url = f'{BASE}/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128'
    body = json.dumps({'text': text, 'model_id': MODEL, 'voice_settings': SETTINGS}).encode()
    req = Request(url, data=body, headers={'xi-api-key': 'board-spend', 'Content-Type': 'application/json'})
    with open(os.path.join(OUT, 'calls.log'), 'a') as log:
        log.write(f'{time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())} {voice} {len(text)} chars {os.path.relpath(path, OUT)}\n')
    try:
        r = json.load(urlopen(req, timeout=300))
    except urllib.error.HTTPError as e:
        sys.exit(f'stopped: HTTP {e.code} {e.read()[:300]!r} on {path}')
    open(path, 'wb').write(base64.b64decode(r['audio_base64']))
    json.dump({'key': key, 'text': text, 'voice': voice, 'model': MODEL, 'settings': SETTINGS, 'alignment': r['alignment']}, open(meta, 'w'))
    return len(text)


def main():
    cmd = sys.argv[1]
    paras = paragraphs()
    excerpt = open(EXCERPT).read().strip()
    if cmd == 'count':
        ch = sum(len(p) for p in paras)
        print(f'casting excerpt: {len(excerpt)} chars per voice; names: {len(NAMES)}; chapter: {ch} chars in {len(paras)} paragraphs')
        return
    os.makedirs(OUT, exist_ok=True)
    spent = 0
    if cmd == 'casting':
        os.makedirs(os.path.join(OUT, 'casting'), exist_ok=True)
        for pair in sys.argv[2:]:
            letter, voice = pair.split('=')
            spent += synth(excerpt, voice, os.path.join(OUT, 'casting', f'{letter}.mp3'))
    elif cmd == 'names':
        spent += synth(NAMES, sys.argv[2], os.path.join(OUT, 'names.mp3'))
    elif cmd == 'chapter':
        os.makedirs(os.path.join(OUT, 'ch1'), exist_ok=True)
        for i, p in enumerate(paras, 1):
            spent += synth(p, sys.argv[2], os.path.join(OUT, 'ch1', f'p{i:03d}.mp3'))
    print(f'paid characters this run: {spent}')


if __name__ == '__main__':
    main()
~~~~

### `tools/voice_mix.py`

~~~~python
"""Voice track for the chapter: every paragraph placed at its time from the timeline, then levelled.

usage: python3 -I tools/voice_mix.py src/chapter1.json voice/ch1 public/chapter1-voice.wav
The timeline must be built with the voice folder (tools/timeline.py ... voice/ch1).
Level: -21 LUFS for the voice alone, true peak -3 dBTP (two-pass loudnorm, linear).
The ambience goes under it in the composition at -6 dB, so it sits 12-18 dB below the voice.
"""
import json
import os
import subprocess
import sys
import wave

import numpy as np

SR = 48000
tl_path, vdir, out = sys.argv[1:4]
tl = json.load(open(tl_path))
if not tl.get('voice'):
    sys.exit('timeline has no voice: build it with the voice folder first')


def ff(*args, capture='stdout'):
    r = subprocess.run(['bunx', 'remotion', 'ffmpeg', '-hide_banner', '-v', 'info' if capture == 'stderr' else 'error', *args], capture_output=True)
    if r.returncode != 0:
        sys.exit(r.stderr.decode()[-2000:])
    return r.stdout if capture == 'stdout' else r.stderr.decode()


track = np.zeros(int(tl['duration'] * SR) + SR, dtype=np.float32)
for v in tl['voice']:
    pcm = ff('-i', os.path.join(vdir, f"p{v['n']:03d}.mp3"), '-f', 's16le', '-ac', '1', '-ar', str(SR), '-')
    x = np.frombuffer(pcm, '<i2').astype(np.float32) / 32768
    a = int(v['start'] * SR)
    track[a:a + len(x)] += x[:len(track) - a]
track = track[:int(tl['duration'] * SR)]

raw = out + '.raw.wav'
with wave.open(raw, 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((np.clip(track, -1, 1) * 32767).astype('<i2').tobytes())

target = 'I=-21:TP=-3:LRA=7'
log = ff('-i', raw, '-af', f'loudnorm={target}:print_format=json', '-f', 'wav', '-y', '/dev/null', capture='stderr')
m = json.loads(log[log.rindex('{'):log.rindex('}') + 1])
ff('-y', '-i', raw, '-af', f"loudnorm={target}:linear=true:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
   f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}",
   '-ar', str(SR), '-ac', '2', out)
os.remove(raw)
print(f"wrote {out}: voice measured {m['input_i']} LUFS, levelled to -21 LUFS")
~~~~

### `tsconfig.json`

~~~~json
{
  "compilerOptions": {
    "target": "ES2018",
    "module": "commonjs",
    "jsx": "react-jsx",
    "strict": true,
    "noEmit": true,
    "lib": ["es2015", "dom"],
    "esModuleInterop": true,
    "resolveJsonModule": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src", "remotion.config.ts"]
}
~~~~

### `../script/chapter-1-dusk.estimated.srt`

~~~~
1
00:00:03,000 --> 00:00:04,570
Part one. Dusk.

2
00:00:06,570 --> 00:00:13,870
It is a Saturday in the middle of January, in the year eighteen ninety-two.

3
00:00:13,870 --> 00:00:23,260
You are on the coast of Maine, at the place where the Penobscot River opens into the bay.

4
00:00:25,260 --> 00:00:33,090
There is a small light station here, on a point of land called Fort Point.

5
00:00:33,090 --> 00:00:37,780
And for this one night, you are its keeper.

6
00:00:39,780 --> 00:00:43,960
You have one task before the day ends.

7
00:00:43,960 --> 00:00:52,300
When the sun goes down, the lamp at the top of the tower must be burning.

8
00:00:54,300 --> 00:00:57,430
Nothing else is required of you.

9
00:00:57,430 --> 00:00:59,520
There is no hurry.

10
00:00:59,520 --> 00:01:07,870
There is only the work, and the evening, and the long winter night that comes after.

11
00:01:10,870 --> 00:01:14,520
So let the day settle around you.

12
00:01:14,520 --> 00:01:16,610
Let your shoulders drop.

13
00:01:16,610 --> 00:01:23,390
We will walk through this evening slowly, one small thing at a time.

14
00:01:27,390 --> 00:01:32,090
The afternoon light in January is low and thin.

15
00:01:32,090 --> 00:01:39,910
It comes across the water at a long angle, and it does not stay long.

16
00:01:41,910 --> 00:01:47,130
Look at the station from the edge of the point.

17
00:01:47,130 --> 00:01:52,350
There is the keeper's house, a wooden house painted white,

18
00:01:52,350 --> 00:01:56,000
with its chimney and its small windows.

19
00:01:58,000 --> 00:02:05,300
And joined to the house, by a narrow room of brick, is the tower.

20
00:02:05,300 --> 00:02:10,000
It is not tall, and it is not round.

21
00:02:10,000 --> 00:02:17,830
It is square, built of brick and painted white, with the glass lantern on top.

22
00:02:19,830 --> 00:02:23,480
That narrow brick room is the workroom.

23
00:02:23,480 --> 00:02:33,390
It means that you can walk from the warm kitchen to the foot of the tower without stepping outside.

24
00:02:33,390 --> 00:02:38,610
On a night like this one, that is a gift.

25
00:02:41,610 --> 00:02:46,830
A light has stood on this point since eighteen thirty-six.

26
00:02:46,830 --> 00:02:53,090
The brick tower you are looking at was built in eighteen fifty-seven.

27
00:02:53,090 --> 00:03:02,480
So it is already older than you might think, and it has seen many winters like this one.

28
00:03:05,480 --> 00:03:14,870
A little way off, about two hundred and fifty feet to the east and north, stands a second,

29
00:03:14,870 --> 00:03:15,910
smaller tower.

30
00:03:15,910 --> 00:03:22,170
It is made of wood, shaped like a pyramid, and painted white.

31
00:03:22,170 --> 00:03:25,300
It is only two years old.

32
00:03:27,300 --> 00:03:30,430
Inside it hangs the fog bell.

33
00:03:30,430 --> 00:03:38,780
When fog comes in over the bay, a machine strikes the bell, once every ten seconds,

34
00:03:38,780 --> 00:03:45,570
so that ships can hear the point even when they cannot see it.

35
00:03:48,570 --> 00:03:54,830
The book of instructions has rules for bell machines like this one.

36
00:03:54,830 --> 00:03:59,520
Never leave the machine alone while it is running;

37
00:03:59,520 --> 00:04:04,220
someone competent must be in constant attendance upon it.

38
00:04:04,220 --> 00:04:11,520
And always take off the winding crank as soon as the machine is wound.

39
00:04:14,520 --> 00:04:18,700
Tonight, we will imagine the air is clear.

40
00:04:18,700 --> 00:04:21,830
The bell will likely stay silent.

41
00:04:24,830 --> 00:04:29,000
Near the station there is a large hotel,

42
00:04:29,000 --> 00:04:34,740
built in the eighteen seventies for summer guests from the cities.

43
00:04:34,740 --> 00:04:41,520
In January, we can picture it closed and dark, its long porches empty,

44
00:04:41,520 --> 00:04:44,130
its rooms waiting for summer.

45
00:04:48,130 --> 00:04:54,910
There is a book of instructions for every keeper in the Light-House Service.

46
00:04:54,910 --> 00:05:00,130
It is small and plain, and it is very clear.

47
00:05:02,130 --> 00:05:07,350
It says that lights must be lighted punctually at sunset,

48
00:05:07,350 --> 00:05:12,570
and must be kept burning at full intensity until sunrise.

49
00:05:15,570 --> 00:05:20,780
It also says that all preparations must be made early,

50
00:05:20,780 --> 00:05:25,480
so that there may be no delay in lighting.

51
00:05:28,480 --> 00:05:31,610
That is why the afternoon matters.

52
00:05:31,610 --> 00:05:37,350
Most of the work of a lighthouse is done in daylight,

53
00:05:37,350 --> 00:05:42,040
so that the moment of lighting can be calm.

54
00:05:45,040 --> 00:05:51,300
Today the sun sets at twenty-three minutes past four, by standard time.

55
00:05:51,300 --> 00:05:57,570
Half an hour later, the last of the twilight will be gone.

56
00:05:59,570 --> 00:06:03,740
You do not need to watch the clock.

57
00:06:03,740 --> 00:06:07,390
You will see it in the sky.

58
00:06:07,390 --> 00:06:11,570
The water darkens first. Then the far shore.

59
00:06:11,570 --> 00:06:15,220
Then the sky, slowly, from the east.

60
00:06:19,220 --> 00:06:22,870
Who keeps a light like this one?

61
00:06:24,870 --> 00:06:30,610
The Light-House Board wrote that at stations needing only one keeper,

62
00:06:30,610 --> 00:06:36,350
it often chose retired sea captains or mates who had families.

63
00:06:38,350 --> 00:06:42,520
So perhaps you have been to sea yourself.

64
00:06:42,520 --> 00:06:52,430
Perhaps you know, from the other side, what it means to see a steady light on a dark shore.

65
00:06:55,430 --> 00:07:03,780
The Board also encouraged its keepers to work small farms or gardens, where the land allowed.

66
00:07:03,780 --> 00:07:09,520
In January, whatever garden there is lies asleep under the cold.

67
00:07:12,520 --> 00:07:21,390
And the pay for this station, in the government register for this year, is five hundred dollars.

68
00:07:25,390 --> 00:07:29,570
The lamp is not in the tower yet.

69
00:07:29,570 --> 00:07:33,220
It is here in the house, waiting.

70
00:07:35,220 --> 00:07:39,910
The book has a rule for very cold weather.

71
00:07:39,910 --> 00:07:45,130
When the lamp is filled and ready for the evening,

72
00:07:45,130 --> 00:07:54,000
it should be kept in a room of moderate temperature, so that the oil does not chill.

73
00:07:57,000 --> 00:08:06,390
So tonight the lamp sits somewhere warm, not too close to the stove, not too far from it.

74
00:08:06,390 --> 00:08:15,780
Let us say it sits on the kitchen table, its brass catching a little of the window light.

75
00:08:18,780 --> 00:08:22,430
It was filled earlier in the day.

76
00:08:22,430 --> 00:08:29,220
The rule says to fill it nearly, but not quite, to the top.

77
00:08:29,220 --> 00:08:36,000
A little room is left, because the oil grows larger as it warms.

78
00:08:39,000 --> 00:08:45,260
You can rest your hand near it and feel nothing at all.

79
00:08:45,260 --> 00:08:48,910
Cold brass. Still oil. A wick waiting.

80
00:08:52,910 --> 00:08:56,040
The lamp burns mineral oil. Kerosene.

81
00:08:56,040 --> 00:09:00,740
By now it is used throughout the lighthouse service.

82
00:09:02,740 --> 00:09:10,570
A book from the Light-House Board, printed in eighteen eighty-nine, compares it with lard oil.

83
00:09:10,570 --> 00:09:19,430
Five gallons of mineral oil, it says, give as much light as four gallons of lard oil,

84
00:09:19,430 --> 00:09:21,520
and cost far less.

85
00:09:24,520 --> 00:09:29,740
The Board set tests for the oil it would accept.

86
00:09:29,740 --> 00:09:36,520
It had to pass a flash test at one hundred and forty degrees,

87
00:09:36,520 --> 00:09:40,700
and stay clear and liquid even at zero.

88
00:09:43,700 --> 00:09:49,430
There are rules about oil, and you keep them without thinking.

89
00:09:49,430 --> 00:09:53,610
The oil must be drawn only by daylight.

90
00:09:53,610 --> 00:09:58,300
Under no circumstances should it be drawn at night.

91
00:10:00,300 --> 00:10:07,090
The cans are kept tightly closed, and the oil room cool and aired.

92
00:10:07,090 --> 00:10:13,350
No one smokes there, and no uncovered light is ever taken there.

93
00:10:15,350 --> 00:10:24,740
And oil is never, ever poured into a lamp while it is lit, or anywhere near a flame.

94
00:10:27,740 --> 00:10:32,960
There is no separate oil house at this station yet.

95
00:10:32,960 --> 00:10:35,570
That will come years later.

96
00:10:35,570 --> 00:10:43,910
So for now, we imagine the cans stored somewhere cool and safe, away from the stove.

97
00:10:47,910 --> 00:10:51,570
By the workroom door hangs your coat.

98
00:10:51,570 --> 00:10:58,350
The service asks its keepers to wear the prescribed uniform at all times.

99
00:11:00,350 --> 00:11:02,960
The cloth is dark blue.

100
00:11:02,960 --> 00:11:09,740
The cap carries a small badge of yellow metal, shaped like a lighthouse.

101
00:11:12,740 --> 00:11:14,830
There are two exceptions.

102
00:11:14,830 --> 00:11:19,520
For outdoor work there is a brown working suit.

103
00:11:19,520 --> 00:11:27,870
And when you clean the lens, the coat comes off, and a linen apron goes on.

104
00:11:29,870 --> 00:11:33,520
The apron is not for your sake.

105
00:11:33,520 --> 00:11:36,130
It is for the glass.

106
00:11:36,130 --> 00:11:41,350
Rough wool could scratch the lens, and linen will not.

107
00:11:44,350 --> 00:11:47,480
This morning, you wore that apron.

108
00:11:47,480 --> 00:11:55,300
You cleaned the lens and the glass of the lantern, as you do every day.

109
00:11:57,300 --> 00:12:03,040
First the feather brush, to lift away every grain of dust.

110
00:12:03,040 --> 00:12:05,650
Then a soft linen cloth.

111
00:12:05,650 --> 00:12:09,830
And last of all, the buff-skin, to polish.

112
00:12:12,830 --> 00:12:22,220
The book warns that a skin which has been wet must never be used, because it will scratch.

113
00:12:22,220 --> 00:12:27,430
So the buff-skin is kept dry, folded, in its place.

114
00:12:31,430 --> 00:12:33,520
It is nearly time.

115
00:12:35,520 --> 00:12:39,700
You put on your coat and your cap.

116
00:12:39,700 --> 00:12:45,430
You take the lamp from the table, carefully, with both hands.

117
00:12:45,430 --> 00:12:48,570
It is heavier than it looks.

118
00:12:51,570 --> 00:12:55,220
You walk through the narrow brick workroom.

119
00:12:55,220 --> 00:12:57,830
Your footsteps sound different here.

120
00:12:57,830 --> 00:12:59,910
The walls are close.

121
00:12:59,910 --> 00:13:06,700
The air is a little colder with every step away from the kitchen.

122
00:13:09,700 --> 00:13:14,910
At the foot of the tower, you begin to climb.

123
00:13:14,910 --> 00:13:19,090
The stairs turn upward in the half dark.

124
00:13:19,090 --> 00:13:23,260
You do not need a light for them.

125
00:13:23,260 --> 00:13:25,350
You know every step.

126
00:13:29,350 --> 00:13:35,610
As you climb, the sounds of the house fall away below you.

127
00:13:35,610 --> 00:13:43,430
Soon there is only your breath, and the stairs, and the wind against the brick.

128
00:13:47,430 --> 00:13:52,130
At the top, you step up into the lantern.

129
00:13:54,130 --> 00:14:00,390
All day, linen curtains have hung around the inside of the glass.

130
00:14:00,390 --> 00:14:07,170
You hung them this morning, when you put out the light at sunrise.

131
00:14:10,170 --> 00:14:12,260
The reason is simple.

132
00:14:12,260 --> 00:14:21,650
A lens that can throw a light sixteen nautical miles across the water can also gather the sun.

133
00:14:21,650 --> 00:14:28,960
Left uncovered on a bright day, it could focus the sunlight and do harm,

134
00:14:28,960 --> 00:14:33,130
and the glass could slowly change its color.

135
00:14:36,130 --> 00:14:39,780
Now, at dusk, the curtains come down.

136
00:14:39,780 --> 00:14:43,430
Keepers took them down in the evening,

137
00:14:43,430 --> 00:14:49,170
so that nothing would stand between the lamp and the water.

138
00:14:52,170 --> 00:14:57,910
You fold them, one at a time. The linen is cold.

139
00:14:57,910 --> 00:15:02,090
The light behind it is grey and blue.

140
00:15:05,090 --> 00:15:07,700
There is another rule here.

141
00:15:07,700 --> 00:15:10,300
While the light is burning,

142
00:15:10,300 --> 00:15:17,090
everything which does not belong in the lantern must be removed from it.

143
00:15:19,090 --> 00:15:26,390
So you carry the curtains down a few steps, and leave them there, folded.

144
00:15:26,390 --> 00:15:31,090
The lantern holds only what it needs. The lens.

145
00:15:31,090 --> 00:15:33,170
The lamp. And you.

146
00:15:37,170 --> 00:15:46,570
Let us look at the lens for a moment, while there is still a little daylight in it.

147
00:15:48,570 --> 00:15:53,260
It is a Fresnel lens, of the fourth order.

148
00:15:53,260 --> 00:16:00,040
The orders are sizes, and the fourth is one of the smaller ones.

149
00:16:03,040 --> 00:16:11,390
It is built of rings of glass prisms, one above another, held in a metal frame.

150
00:16:11,390 --> 00:16:17,130
The prisms bend and reflect the light of one small flame,

151
00:16:17,130 --> 00:16:24,430
rays that would scatter in every direction, and send them out toward the water.

152
00:16:27,430 --> 00:16:33,700
At this station, the light does not turn and does not flash.

153
00:16:33,700 --> 00:16:36,830
It is a fixed white light.

154
00:16:36,830 --> 00:16:39,960
It simply shines, steady, all night.

155
00:16:42,960 --> 00:16:51,300
A ship coming up the bay will see it as a single, still point of white,

156
00:16:51,300 --> 00:16:54,430
marking the way into the river.

157
00:16:58,430 --> 00:17:01,040
The sun is down now.

158
00:17:01,040 --> 00:17:09,910
The water has gone dark, and the sky over the far shore is the color of ashes.

159
00:17:12,910 --> 00:17:21,780
The book says the lamp must be placed inside the lens, in its place, and then lighted.

160
00:17:23,780 --> 00:17:31,090
So you set it down, gently, at the very center of all that glass.

161
00:17:34,090 --> 00:17:38,780
You strike a match. The wick takes the flame.

162
00:17:42,780 --> 00:17:47,480
And now comes the part that cannot be hurried.

163
00:17:49,480 --> 00:17:55,220
For the first half hour, the flame must be kept low.

164
00:17:55,220 --> 00:18:00,430
The glass chimney of the lamp has to warm slowly.

165
00:18:00,430 --> 00:18:08,780
If you turn the wick up too soon, before the chimney and the burner are warm,

166
00:18:08,780 --> 00:18:10,870
the lamp will smoke.

167
00:18:14,870 --> 00:18:17,480
So you keep it low.

168
00:18:17,480 --> 00:18:22,700
A small flame, in the middle of the great glass.

169
00:18:25,700 --> 00:18:29,350
And slowly, the lens begins to fill.

170
00:18:29,350 --> 00:18:36,130
Ring after ring takes the light, until the whole lantern glows with it.

171
00:18:41,130 --> 00:18:46,870
From the gallery outside, if you stepped out into the cold,

172
00:18:46,870 --> 00:18:55,220
you would see the light laid out over the water, low and level, toward the ships.

173
00:18:58,220 --> 00:19:04,480
It will burn now until sunrise, at full strength, without a break.

174
00:19:07,480 --> 00:19:13,740
The Weather Bureau's map for this evening shows clearing weather moving east,

175
00:19:13,740 --> 00:19:19,480
toward New England, and the forecast for tomorrow is generally fair.

176
00:19:19,480 --> 00:19:22,610
At Eastport, further along the coast,

177
00:19:22,610 --> 00:19:28,350
the thermometer will read ten degrees above zero at eight o'clock.

178
00:19:30,350 --> 00:19:37,650
Here at the point, we can imagine the same: a cold, still, clear night.

179
00:19:40,650 --> 00:19:44,830
The stars are coming out over the bay.

180
00:19:44,830 --> 00:19:54,220
And in about two and a half hours, a moon just past full will rise in the east,

181
00:19:54,220 --> 00:19:58,910
and lay its own pale road across the water.

182
00:20:02,910 --> 00:20:10,220
The list of lights for these years gives no winter pause for this station.

183
00:20:10,220 --> 00:20:21,170
The rules say a light must always be shown if it is at all possible for vessels to benefit by it.

184
00:20:25,170 --> 00:20:27,260
The lamp is lit.

185
00:20:27,260 --> 00:20:31,960
The hardest part of the evening is already done.

186
00:20:34,960 --> 00:20:42,260
The government register for this year lists one name at this station, the keeper's.

187
00:20:42,260 --> 00:20:44,350
No assistant is listed.

188
00:20:46,350 --> 00:20:55,740
For a keeper alone, the book says, the light must be visited at least twice during the night,

189
00:20:55,740 --> 00:20:58,350
between eight o'clock and sunrise.

190
00:20:58,350 --> 00:21:03,570
And on stormy nights, it must be constantly looked after.

191
00:21:06,570 --> 00:21:09,700
Tonight is not a stormy night.

192
00:21:09,700 --> 00:21:15,960
So you will climb these stairs twice more, in the dark hours.

193
00:21:15,960 --> 00:21:17,520
That is all.

194
00:21:20,520 --> 00:21:24,700
The station must never be left wholly unattended.

195
00:21:24,700 --> 00:21:33,570
If a keeper must be away, a member of his family, or another responsible person, must stay.

196
00:21:36,570 --> 00:21:40,740
Later this evening, you will open the journal.

197
00:21:40,740 --> 00:21:47,000
Each day takes one line, written across both pages, in ink, neatly.

198
00:21:47,000 --> 00:21:53,260
The weather goes in it, and anything of interest on the water.

199
00:21:56,260 --> 00:22:01,480
One line for a whole day. It seems very little.

200
00:22:01,480 --> 00:22:06,170
But on a quiet day, one line is enough.

201
00:22:09,170 --> 00:22:10,740
Tomorrow is Sunday.

202
00:22:10,740 --> 00:22:17,520
The rules allow a keeper to be away on Sundays to attend church,

203
00:22:17,520 --> 00:22:24,300
so long as the light is never left without someone to watch it.

204
00:22:27,300 --> 00:22:29,390
But that is tomorrow.

205
00:22:29,390 --> 00:22:32,000
Tonight there is only tonight.

206
00:22:36,000 --> 00:22:40,700
So the first part of the night is done.

207
00:22:43,700 --> 00:22:48,910
The lamp is burning low and steady, warming its glass.

208
00:22:48,910 --> 00:22:51,520
The kitchen is warm below.

209
00:22:51,520 --> 00:22:54,650
The bay is dark and calm.

210
00:22:57,650 --> 00:23:01,830
There is nothing you need to do now.

211
00:23:01,830 --> 00:23:04,430
Nothing you need to remember.

212
00:23:07,430 --> 00:23:15,260
Just the light above you, keeping its watch, so that you do not have to.

213
00:23:20,260 --> 00:23:21,300
Rest now.
~~~~
