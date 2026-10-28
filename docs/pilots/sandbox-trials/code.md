# Код пилота Sandbox Trials

Весь код расчёта и рендера Event 1. В docs нельзя класть файлы кода, поэтому он хранится здесь текстом. Каждый раздел — один файл: заголовок — путь от папки projects/pilots/sandbox-trials. Как разложить по файлам — в README.md, раздел «С чего продолжить».

## .gitignore

~~~~text
node_modules/
deps/
out/
~~~~

## package.json

~~~~json
{
  "name": "sandbox-trials-pilot",
  "private": true,
  "type": "module",
  "dependencies": {
    "@napi-rs/canvas": "1.0.9",
    "ffmpeg-static": "5.3.0"
  },
  "trustedDependencies": ["ffmpeg-static"]
}
~~~~

## bun.lock

~~~~json
{
  "lockfileVersion": 2,
  "configVersion": 1,
  "workspaces": {
    "": {
      "name": "sandbox-trials-pilot",
      "dependencies": {
        "@napi-rs/canvas": "1.0.9",
        "ffmpeg-static": "5.3.0",
      },
    },
  },
  "trustedDependencies": [
    "ffmpeg-static",
  ],
  "packages": {
    "@derhuerst/http-basic": ["@derhuerst/http-basic@8.2.4", "", { "dependencies": { "caseless": "^0.12.0", "concat-stream": "^2.0.0", "http-response-object": "^3.0.1", "parse-cache-control": "^1.0.1" } }, "sha512-F9rL9k9Xjf5blCz8HsJRO4diy111cayL2vkY2XE4r4t3n0yPXVYy3KD3nJ1qbrSn9743UWSXH4IwuCa/HWlGFw=="],

    "@napi-rs/canvas": ["@napi-rs/canvas@1.0.9", "", { "optionalDependencies": { "@napi-rs/canvas-android-arm64": "1.0.9", "@napi-rs/canvas-darwin-arm64": "1.0.9", "@napi-rs/canvas-darwin-x64": "1.0.9", "@napi-rs/canvas-linux-arm-gnueabihf": "1.0.9", "@napi-rs/canvas-linux-arm64-gnu": "1.0.9", "@napi-rs/canvas-linux-arm64-musl": "1.0.9", "@napi-rs/canvas-linux-riscv64-gnu": "1.0.9", "@napi-rs/canvas-linux-x64-gnu": "1.0.9", "@napi-rs/canvas-linux-x64-musl": "1.0.9", "@napi-rs/canvas-win32-arm64-msvc": "1.0.9", "@napi-rs/canvas-win32-x64-msvc": "1.0.9" } }, "sha512-QviPdJImDi/jMAvBfqaw+19BndMd/sizXVW3NnpMd3VJGz++QXkOHcP9kWR/smHG0hNjHeyuHFyrx/5lD0oNcQ=="],

    "@napi-rs/canvas-android-arm64": ["@napi-rs/canvas-android-arm64@1.0.9", "", { "os": "android", "cpu": "arm64" }, "sha512-4LGXk2/0HVzE29K8SzML5WubgCp++B1FH3qgl35XmSZE+lLdr6P9VRQEnZ0MCLZMTSuJP41yyhtoiVNEuvrTIA=="],

    "@napi-rs/canvas-darwin-arm64": ["@napi-rs/canvas-darwin-arm64@1.0.9", "", { "os": "darwin", "cpu": "arm64" }, "sha512-YNdfLBzY0W/Pep9fo2L6RmoNlNksnn05LRnX66W63R3ij58S25QOTcjdtEt2v8+PnCESzqZsYzUo+QPeIR44NA=="],

    "@napi-rs/canvas-darwin-x64": ["@napi-rs/canvas-darwin-x64@1.0.9", "", { "os": "darwin", "cpu": "x64" }, "sha512-ceZQSknTEcy3dOXoekv59LTCkXjvnLsq+VW5PeNNDHEPQbRS5Ervkm1EaDa7WLAjiYWMLuSQTRTHao1dEX4prg=="],

    "@napi-rs/canvas-linux-arm-gnueabihf": ["@napi-rs/canvas-linux-arm-gnueabihf@1.0.9", "", { "os": "linux", "cpu": "arm" }, "sha512-XhfI0Wwv4llhd6nnWDtY3kQKjq0r+y1i91PlJlJI24ag2U9WrnwbG1qS3+fDLEyouwEVFchiKkTEHozK+5iUNA=="],

    "@napi-rs/canvas-linux-arm64-gnu": ["@napi-rs/canvas-linux-arm64-gnu@1.0.9", "", { "os": "linux", "cpu": "arm64" }, "sha512-012oiYtKaE7i9oxc8q7nraT7kDOpLcaCmFLzVe9Ty34RHDdoDzbWLrVh827CNxYh/EADX1eSikA3ymLjo/nNuw=="],

    "@napi-rs/canvas-linux-arm64-musl": ["@napi-rs/canvas-linux-arm64-musl@1.0.9", "", { "os": "linux", "cpu": "arm64" }, "sha512-Ls5UWYFFn63casTZEczbeyEg3vRDRkv9lscuGwfchtY5yLLQhgOB8SN4YGxmfJ5vTaBwZ2YUxBS3NtmjJmFXdA=="],

    "@napi-rs/canvas-linux-riscv64-gnu": ["@napi-rs/canvas-linux-riscv64-gnu@1.0.9", "", { "os": "linux", "cpu": "none" }, "sha512-hLKEGxV7ZiRHqndePTokgDMdBlo/rDfzg7P4p4QIv9pUhuYobnu3R2NIFLCRghG0nwfo+s2sw+c1xZFeCmEAsw=="],

    "@napi-rs/canvas-linux-x64-gnu": ["@napi-rs/canvas-linux-x64-gnu@1.0.9", "", { "os": "linux", "cpu": "x64" }, "sha512-6kaz3w0QMy77PDWk6rJ1ksIihdad3qzEyX2o2oGT8GwCaypfT5mhjr8buOO5hstyLxcWXDScuz56RsINLtBPIQ=="],

    "@napi-rs/canvas-linux-x64-musl": ["@napi-rs/canvas-linux-x64-musl@1.0.9", "", { "os": "linux", "cpu": "x64" }, "sha512-xrGvmS3v55hmZ86ls/kBLVNMUTYio3f6Ik0DireemG994VfPAwiA3ZXA0Uf1bByctkB3NQ1Sfb+H5bkdUnnzfQ=="],

    "@napi-rs/canvas-win32-arm64-msvc": ["@napi-rs/canvas-win32-arm64-msvc@1.0.9", "", { "os": "win32", "cpu": "arm64" }, "sha512-yjmVS3ArZeRVCP7jqbPq4rpZa/BhTeI7ELE2XqJg3snICQBDevLZyArxswHkiTnT34KRic33/4fLirrHI+SY8A=="],

    "@napi-rs/canvas-win32-x64-msvc": ["@napi-rs/canvas-win32-x64-msvc@1.0.9", "", { "os": "win32", "cpu": "x64" }, "sha512-QlSYQdMQslB81nlABo9wNfQ6npFhE7/O+saCZdqVGueGanyRk4jCogD5EwQenfP3kIq9e+mm6GreQBjX5MrA8g=="],

    "@types/node": ["@types/node@10.17.60", "", {}, "sha512-F0KIgDJfy2nA3zMLmWGKxcH2ZVEtCZXHHdOQs2gSaQ27+lNeEfGxzkIw90aXswATX7AZ33tahPbzy6KAfUreVw=="],

    "agent-base": ["agent-base@6.0.2", "", { "dependencies": { "debug": "4" } }, "sha512-RZNwNclF7+MS/8bDg70amg32dyeZGZxiDuQmZxKLAlQjr3jGyLx+4Kkk58UO7D2QdgFIQCovuSuZESne6RG6XQ=="],

    "buffer-from": ["buffer-from@1.1.2", "", {}, "sha512-E+XQCRwSbaaiChtv6k6Dwgc+bx+Bs6vuKJHHl5kox/BaKbhiXzqQOwK4cO22yElGp2OCmjwVhT3HmxgyPGnJfQ=="],

    "caseless": ["caseless@0.12.0", "", {}, "sha512-4tYFyifaFfGacoiObjJegolkwSU4xQNGbVgUiNYVUxbQ2x2lUsFvY4hVgVzGiIe6WLOPqycWXA40l+PWsxthUw=="],

    "concat-stream": ["concat-stream@2.0.0", "", { "dependencies": { "buffer-from": "^1.0.0", "inherits": "^2.0.3", "readable-stream": "^3.0.2", "typedarray": "^0.0.6" } }, "sha512-MWufYdFw53ccGjCA+Ol7XJYpAlW6/prSMzuPOTRnJGcGzuhLn4Scrz7qf6o8bROZ514ltazcIFJZevcfbo0x7A=="],

    "debug": ["debug@4.4.3", "", { "dependencies": { "ms": "^2.1.3" }, "peerDependencies": { "supports-color": "*" }, "optionalPeers": ["supports-color"] }, "sha512-RGwwWnwQvkVfavKVt22FGLw+xYSdzARwm0ru6DhTVA3umU5hZc28V3kO4stgYryrTlLpuvgI9GiijltAjNbcqA=="],

    "env-paths": ["env-paths@2.2.1", "", {}, "sha512-+h1lkLKhZMTYjog1VEpJNG7NZJWcuc2DDk/qsqSTRRCOXiLjeQ1d1/udrUGhqMxUgAlwKNZ0cf2uqan5GLuS2A=="],

    "ffmpeg-static": ["ffmpeg-static@5.3.0", "", { "dependencies": { "@derhuerst/http-basic": "^8.2.0", "env-paths": "^2.2.0", "https-proxy-agent": "^5.0.0", "progress": "^2.0.3" } }, "sha512-H+K6sW6TiIX6VGend0KQwthe+kaceeH/luE8dIZyOP35ik7ahYojDuqlTV1bOrtEwl01sy2HFNGQfi5IDJvotg=="],

    "http-response-object": ["http-response-object@3.0.2", "", { "dependencies": { "@types/node": "^10.0.3" } }, "sha512-bqX0XTF6fnXSQcEJ2Iuyr75yVakyjIDCqroJQ/aHfSdlM743Cwqoi2nDYMzLGWUcuTWGWy8AAvOKXTfiv6q9RA=="],

    "https-proxy-agent": ["https-proxy-agent@5.0.1", "", { "dependencies": { "agent-base": "6", "debug": "4" } }, "sha512-dFcAjpTQFgoLMzC2VwU+C/CbS7uRL0lWmxDITmqm7C+7F0Odmj6s9l6alZc6AELXhrnggM2CeWSXHGOdX2YtwA=="],

    "inherits": ["inherits@2.0.4", "", {}, "sha512-k/vGaX4/Yla3WzyMCvTQOXYeIHvqOKtnqBduzTHpzpQZzAskKMhZ2K+EnBiSM9zGSoIFeMpXKxa4dYeZIQqewQ=="],

    "ms": ["ms@2.1.3", "", {}, "sha512-6FlzubTLZG3J2a/NVCAleEhjzq5oxgHyaCU9yYXvcLsvoVaHJq/s5xXI6/XXP6tz7R9xAOtHnSO/tXtF3WRTlA=="],

    "parse-cache-control": ["parse-cache-control@1.0.1", "", {}, "sha512-60zvsJReQPX5/QP0Kzfd/VrpjScIQ7SHBW6bFCYfEP+fp0Eppr1SHhIO5nd1PjZtvclzSzES9D/p5nFJurwfWg=="],

    "progress": ["progress@2.0.3", "", {}, "sha512-7PiHtLll5LdnKIMw100I+8xJXR5gW2QwWYkT6iJva0bXitZKa/XMrSbdmg3r2Xnaidz9Qumd0VPaMrZlF9V9sA=="],

    "readable-stream": ["readable-stream@3.6.2", "", { "dependencies": { "inherits": "^2.0.3", "string_decoder": "^1.1.1", "util-deprecate": "^1.0.1" } }, "sha512-9u/sniCrY3D5WdsERHzHE4G2YCXqoG5FTHUiCC4SIbr6XcLZBY05ya9EKjYek9O5xOAwjGq+1JdGBAS7Q9ScoA=="],

    "safe-buffer": ["safe-buffer@5.2.1", "", {}, "sha512-rp3So07KcdmmKbGvgaNxQSJr7bGVSVk5S9Eq1F+ppbRo70+YeaDxkw5Dd8NPN+GD6bjnYm2VuPuCXmpuYvmCXQ=="],

    "string_decoder": ["string_decoder@1.3.0", "", { "dependencies": { "safe-buffer": "~5.2.0" } }, "sha512-hkRX8U1WjJFd8LsDJ2yQ/wWWxaopEsABU1XfkM8A+j0+85JAGppt16cr1Whg6KIbb4okU6Mql6BOj+uup/wKeA=="],

    "typedarray": ["typedarray@0.0.6", "", {}, "sha512-/aCDEGatGvZ2BIk+HmLf4ifCJFwvKFNb9/JeZPMulfgFracn9QFcAf5GO8B/mweUjSoblS5In0cWhqpfs/5PQA=="],

    "util-deprecate": ["util-deprecate@1.0.2", "", {}, "sha512-EPD5q1uXyFxJpCrLnCc1nHnq3gOa6DZBocAIiI2TaSCA7VCJ1UJDMagCzIkXNsUYfD1daK//LTEQ8xiIbrHtcw=="],
  }
}
~~~~

## sim/build.sh

~~~~bash
#!/usr/bin/env bash
# Fetches Box2D v3.1.1 (checked by sha256) and builds the league simulator.
# Flags follow Box2D's own CMake: -ffp-contract=off for cross-platform determinism.
set -euo pipefail
cd "$(dirname "$0")/.."
B2=deps/box2d-3.1.1
if [ ! -d "$B2" ]; then
  mkdir -p deps
  curl -sSL -o deps/box2d-3.1.1.tar.gz https://codeload.github.com/erincatto/box2d/tar.gz/refs/tags/v3.1.1
  echo "fb6ef914b50f4312d7d921a600eabc12318bb3c55a0b8c0b90608fa4488ef2e4  deps/box2d-3.1.1.tar.gz" | sha256sum -c -
  tar xzf deps/box2d-3.1.1.tar.gz -C deps
fi
FLAGS="-O2 -std=gnu17 -ffp-contract=off -DNDEBUG -I $B2/include -I $B2/src"
mkdir -p deps/build
for c in "$B2"/src/*.c; do echo "$c"; done | xargs -P4 -I{} sh -c "gcc $FLAGS -c {} -o deps/build/\$(basename {} .c).o"
ar rcs deps/build/libbox2d.a deps/build/*.o
gcc $FLAGS sim/league.c deps/build/libbox2d.a -lm -lpthread -o deps/league
echo "built deps/league"
~~~~

## sim/league.c

~~~~c
// Sandbox Trials league simulator on Box2D v3.1.1.
// Reads a flat scene file written by sim/build-scene.ts, runs one seed or a batch.
//
//   league scene.txt run <seed> [frames.bin] [hits.csv]   one run, JSON result on stdout
//   league scene.txt batch <from> <to>          one CSV line per seed:
//     seed, hash, steps, leader changes, then name:finish time for each shape in finishing order
//
// Randomness comes only from the seed: the hopper slot of each shape and a
// small jitter of its start position and angle. Nothing else is random.

#include "box2d/box2d.h"

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_BODIES 32
#define MAX_GATES 8
#define MAX_PARTS 4

typedef struct
{
	char name[16];
	char kind[16];
	int partCount;
	float a[MAX_PARTS][16]; // shape parameters per part, see parse
	int vertexCount;
	float density, friction, restitution, rolling;
	int hasCom;
	float comX, comY;
	b2BodyId id;
	int finished;
	double finishTime;
} Racer;

typedef struct
{
	b2ShapeId id;
	float openTime;
	int open;
} Gate;

static Racer racers[MAX_BODIES];
static int racerCount;
static Gate gates[MAX_GATES];
static int gateCount;

static float gravityY = -9.8f;
static float duration = 120.0f;
static int hz = 60, substeps = 4;
static float slotX[MAX_BODIES], slotY[MAX_BODIES];
static int slotCount;
static float jitter = 0.05f;
static float finishX, finishY0, finishY1;
static int finishDir = 1;

typedef struct
{
	char line[512];
} Line;
static Line staticLines[2048];
static int staticCount;

// splitmix64: integer-only, same result on every platform
static uint64_t rngState;
static uint64_t Next( void )
{
	uint64_t z = ( rngState += 0x9E3779B97F4A7C15ull );
	z = ( z ^ ( z >> 30 ) ) * 0xBF58476D1CE4E5B9ull;
	z = ( z ^ ( z >> 27 ) ) * 0x94D049BB133111EBull;
	return z ^ ( z >> 31 );
}
static float Uniform( void )
{
	return (float)( Next() >> 40 ) / (float)( 1ull << 24 ); // [0,1) on a 24-bit grid
}

static void Fail( const char* msg )
{
	fprintf( stderr, "league: %s\n", msg );
	exit( 1 );
}

static void Parse( const char* path )
{
	FILE* f = fopen( path, "r" );
	if ( f == NULL )
		Fail( "cannot open scene" );
	char line[512];
	while ( fgets( line, sizeof line, f ) )
	{
		char key[32];
		if ( sscanf( line, "%31s", key ) != 1 || key[0] == '#' )
			continue;
		if ( strcmp( key, "world" ) == 0 )
			sscanf( line, "%*s %f %f %d %d", &gravityY, &duration, &hz, &substeps );
		else if ( strcmp( key, "slot" ) == 0 )
		{
			sscanf( line, "%*s %f %f", &slotX[slotCount], &slotY[slotCount] );
			slotCount++;
		}
		else if ( strcmp( key, "jitter" ) == 0 )
			sscanf( line, "%*s %f", &jitter );
		else if ( strcmp( key, "finish" ) == 0 )
			sscanf( line, "%*s %f %f %f %d", &finishX, &finishY0, &finishY1, &finishDir );
		else if ( strcmp( key, "seg" ) == 0 || strcmp( key, "peg" ) == 0 || strcmp( key, "gate" ) == 0 )
		{
			if ( staticCount >= 2048 )
				Fail( "too many static parts" );
			strcpy( staticLines[staticCount++].line, line );
		}
		else if ( strcmp( key, "racer" ) == 0 )
		{
			if ( racerCount >= MAX_BODIES )
				Fail( "too many racers" );
			Racer* r = racers + racerCount++;
			memset( r, 0, sizeof *r );
			int n = 0;
			sscanf( line, "%*s %15s %15s %f %f %f %f %n", r->name, r->kind, &r->density, &r->friction, &r->restitution,
					&r->rolling, &n );
			const char* p = line + n;
			// remaining numbers: shape parameters, then optional "com x y"
			float v[40];
			int vc = 0, used;
			while ( vc < 40 && sscanf( p, "%f%n", &v[vc], &used ) == 1 )
			{
				p += used;
				vc++;
			}
			if ( strstr( p, "com" ) )
			{
				r->hasCom = 1;
				sscanf( strstr( p, "com" ), "com %f %f", &r->comX, &r->comY );
			}
			r->partCount = 1;
			for ( int i = 0; i < vc && i < 16; i++ )
				r->a[0][i] = v[i];
			r->vertexCount = vc / 2;
			if ( strcmp( r->kind, "poly" ) == 0 && vc > 16 )
				Fail( "polygon has more than 8 vertices" );
		}
	}
	fclose( f );
	if ( slotCount < racerCount )
		Fail( "fewer start slots than racers" );
}

static void BuildStatic( b2WorldId world )
{
	b2BodyDef bd = b2DefaultBodyDef();
	b2BodyId ground = b2CreateBody( world, &bd );
	gateCount = 0;
	for ( int i = 0; i < staticCount; i++ )
	{
		const char* line = staticLines[i].line;
		char key[16];
		float x1, y1, x2, y2, fr, re, t;
		b2ShapeDef sd = b2DefaultShapeDef();
		sscanf( line, "%15s", key );
		if ( strcmp( key, "peg" ) == 0 )
		{
			sscanf( line, "%*s %f %f %f %f %f", &x1, &y1, &x2, &fr, &re );
			sd.material.friction = fr;
			sd.material.restitution = re;
			b2Circle c = { { x1, y1 }, x2 };
			b2CreateCircleShape( ground, &sd, &c );
			continue;
		}
		if ( strcmp( key, "gate" ) == 0 )
			sscanf( line, "%*s %f %f %f %f %f %f %f", &x1, &y1, &x2, &y2, &fr, &re, &t );
		else
			sscanf( line, "%*s %f %f %f %f %f %f", &x1, &y1, &x2, &y2, &fr, &re );
		sd.material.friction = fr;
		sd.material.restitution = re;
		b2Segment s = { { x1, y1 }, { x2, y2 } };
		b2ShapeId id = b2CreateSegmentShape( ground, &sd, &s );
		if ( strcmp( key, "gate" ) == 0 )
		{
			if ( gateCount >= MAX_GATES )
				Fail( "too many gates" );
			gates[gateCount].id = id;
			gates[gateCount].openTime = t;
			gates[gateCount].open = 0;
			gateCount++;
		}
	}
}

static void BuildRacer( b2WorldId world, Racer* r, float x, float y, float angle )
{
	b2BodyDef bd = b2DefaultBodyDef();
	bd.type = b2_dynamicBody;
	bd.position = ( b2Vec2 ){ x, y };
	bd.rotation = b2MakeRot( angle );
	r->id = b2CreateBody( world, &bd );
	b2ShapeDef sd = b2DefaultShapeDef();
	sd.density = r->density;
	sd.material.friction = r->friction;
	sd.material.restitution = r->restitution;
	sd.material.rollingResistance = r->rolling;
	sd.enableHitEvents = true; // reporting only, the sound track is built from these
	sd.userData = (void*)( r - racers + 1 );
	float* a = r->a[0];
	if ( strcmp( r->kind, "circle" ) == 0 )
	{
		b2Circle c = { { 0, 0 }, a[0] };
		b2CreateCircleShape( r->id, &sd, &c );
	}
	else if ( strcmp( r->kind, "twin" ) == 0 )
	{
		// two balls of radius a[0] at +-a[1] on one body, joined by a thin bar
		b2Circle c1 = { { -a[1], 0 }, a[0] }, c2 = { { a[1], 0 }, a[0] };
		b2CreateCircleShape( r->id, &sd, &c1 );
		b2CreateCircleShape( r->id, &sd, &c2 );
		b2Polygon bar = b2MakeBox( a[1], a[0] * 0.35f );
		b2CreatePolygonShape( r->id, &sd, &bar );
	}
	else if ( strcmp( r->kind, "capsule" ) == 0 )
	{
		b2Capsule c = { { -a[0], 0 }, { a[0], 0 }, a[1] };
		b2CreateCapsuleShape( r->id, &sd, &c );
	}
	else if ( strcmp( r->kind, "poly" ) == 0 )
	{
		b2Vec2 pts[8];
		for ( int i = 0; i < r->vertexCount; i++ )
			pts[i] = ( b2Vec2 ){ a[2 * i], a[2 * i + 1] };
		b2Hull hull = b2ComputeHull( pts, r->vertexCount );
		if ( hull.count == 0 )
			Fail( "bad polygon hull" );
		b2Polygon poly = b2MakePolygon( &hull, 0.0f );
		b2CreatePolygonShape( r->id, &sd, &poly );
	}
	else
		Fail( "unknown racer kind" );
	if ( r->hasCom )
	{
		// move the centre of mass, keep mass; inertia about the new centre
		b2MassData m = b2Body_GetMassData( r->id );
		float d2 = r->comX * r->comX + r->comY * r->comY;
		float inertiaAtCentre = m.rotationalInertia - m.mass * ( m.center.x * m.center.x + m.center.y * m.center.y );
		m.center = ( b2Vec2 ){ r->comX, r->comY };
		m.rotationalInertia = inertiaAtCentre + m.mass * d2;
		b2Body_SetMassData( r->id, m );
	}
}

typedef struct
{
	int order[MAX_BODIES];
	int steps;
	int leaderChanges;
	uint64_t hash;
} Result;

static uint64_t HashFloat( uint64_t h, float v )
{
	uint32_t bits;
	memcpy( &bits, &v, 4 );
	for ( int i = 0; i < 4; i++ )
	{
		h ^= ( bits >> ( 8 * i ) ) & 0xff;
		h *= 0x100000001B3ull;
	}
	return h;
}

static Result Run( uint64_t seed, FILE* frames, FILE* hits )
{
	rngState = seed;
	b2WorldDef wd = b2DefaultWorldDef();
	wd.gravity = ( b2Vec2 ){ 0, gravityY };
	wd.enableSleep = false;
	b2WorldId world = b2CreateWorld( &wd );
	BuildStatic( world );

	// seeded shuffle of start slots (Fisher-Yates)
	int slot[MAX_BODIES];
	for ( int i = 0; i < slotCount; i++ )
		slot[i] = i;
	for ( int i = slotCount - 1; i > 0; i-- )
	{
		int j = (int)( Next() % (uint64_t)( i + 1 ) );
		int t = slot[i];
		slot[i] = slot[j];
		slot[j] = t;
	}
	for ( int i = 0; i < racerCount; i++ )
	{
		float jx = ( Uniform() * 2 - 1 ) * jitter, jy = ( Uniform() * 2 - 1 ) * jitter;
		float ang = Uniform() * 6.2831853f;
		racers[i].finished = 0;
		racers[i].finishTime = 0;
		BuildRacer( world, racers + i, slotX[slot[i]] + jx, slotY[slot[i]] + jy, ang );
	}

	if ( frames )
	{
		int32_t header[3] = { racerCount, hz, 0 };
		fwrite( header, 4, 3, frames );
	}

	float dt = 1.0f / (float)hz;
	int maxSteps = (int)( duration * (float)hz );
	int finishedCount = 0, step = 0;
	float prevX[MAX_BODIES];
	for ( int i = 0; i < racerCount; i++ )
		prevX[i] = b2Body_GetPosition( racers[i].id ).x;
	// leader = lowest centre on the course (finished shapes are below the finish); a new
	// leader counts only after holding the lead for 0.5 s, so touch-and-go swaps are not counted
	int leader = -1, candidate = -1, candidateSince = 0, leaderChanges = 0;
	const int hold = hz / 2;
	for ( step = 0; step < maxSteps && finishedCount < racerCount; step++ )
	{
		float t = (float)step * dt;
		for ( int g = 0; g < gateCount; g++ )
			if ( !gates[g].open && t >= gates[g].openTime )
			{
				b2DestroyShape( gates[g].id, false );
				gates[g].open = 1;
			}
		b2World_Step( world, dt, substeps );
		if ( hits )
		{
			// step, shape a, shape b (0 = track), approach speed m/s, x, y
			b2ContactEvents ev = b2World_GetContactEvents( world );
			for ( int h = 0; h < ev.hitCount; h++ )
			{
				b2ContactHitEvent* e = ev.hitEvents + h;
				fprintf( hits, "%d,%d,%d,%.3f,%.3f,%.3f\n", step, (int)(intptr_t)b2Shape_GetUserData( e->shapeIdA ),
						 (int)(intptr_t)b2Shape_GetUserData( e->shapeIdB ), e->approachSpeed, e->point.x, e->point.y );
			}
		}
		for ( int i = 0; i < racerCount; i++ )
		{
			b2Vec2 p = b2Body_GetPosition( racers[i].id );
			b2Rot q = b2Body_GetRotation( racers[i].id );
			if ( frames )
			{
				float rec[3] = { p.x, p.y, b2Rot_GetAngle( q ) };
				fwrite( rec, 4, 3, frames );
			}
			if ( !racers[i].finished && p.y >= finishY0 && p.y <= finishY1 &&
				 ( finishDir > 0 ? ( prevX[i] < finishX && p.x >= finishX ) : ( prevX[i] > finishX && p.x <= finishX ) ) )
			{
				// crossing time interpolated inside the step
				double f = ( finishX - prevX[i] ) / (double)( p.x - prevX[i] );
				racers[i].finished = 1;
				racers[i].finishTime = ( (double)step + f ) * dt;
				finishedCount++;
			}
			prevX[i] = p.x;
		}
		int low = 0;
		for ( int i = 1; i < racerCount; i++ )
			if ( b2Body_GetPosition( racers[i].id ).y < b2Body_GetPosition( racers[low].id ).y )
				low = i;
		if ( low != candidate )
		{
			candidate = low;
			candidateSince = step;
		}
		// counting starts 1 s after the first gate opens: settling in the pile is not a lead change
		int racing = gateCount == 0 || t >= gates[0].openTime + 1.0f;
		if ( racing && candidate != leader && step - candidateSince >= hold && finishedCount == 0 )
		{
			if ( leader >= 0 )
				leaderChanges++;
			leader = candidate;
		}
	}

	Result res;
	res.steps = step;
	res.leaderChanges = leaderChanges;
	uint64_t h = 0xCBF29CE484222325ull;
	for ( int i = 0; i < racerCount; i++ )
	{
		b2Vec2 p = b2Body_GetPosition( racers[i].id );
		b2Rot q = b2Body_GetRotation( racers[i].id );
		h = HashFloat( h, p.x );
		h = HashFloat( h, p.y );
		h = HashFloat( h, q.c );
		h = HashFloat( h, q.s );
		res.order[i] = i;
	}
	res.hash = h;
	// finished first by time; the rest by height, lower is further down the course
	for ( int i = 0; i < racerCount; i++ )
		for ( int j = i + 1; j < racerCount; j++ )
		{
			Racer *a = racers + res.order[i], *b = racers + res.order[j];
			int swap;
			if ( a->finished != b->finished )
				swap = b->finished;
			else if ( a->finished )
				swap = b->finishTime < a->finishTime;
			else
				swap = b2Body_GetPosition( b->id ).y < b2Body_GetPosition( a->id ).y;
			if ( swap )
			{
				int t = res.order[i];
				res.order[i] = res.order[j];
				res.order[j] = t;
			}
		}
	if ( frames )
	{
		fseek( frames, 8, SEEK_SET );
		int32_t n = step;
		fwrite( &n, 4, 1, frames );
	}
	b2DestroyWorld( world );
	return res;
}

int main( int argc, char** argv )
{
	if ( argc < 4 )
		Fail( "usage: league scene.txt run <seed> [frames.bin] | batch <from> <to>" );
	Parse( argv[1] );
	if ( strcmp( argv[2], "run" ) == 0 )
	{
		uint64_t seed = strtoull( argv[3], NULL, 10 );
		FILE* frames = argc > 4 ? fopen( argv[4], "wb" ) : NULL;
		FILE* hits = argc > 5 ? fopen( argv[5], "w" ) : NULL;
		Result r = Run( seed, frames, hits );
		if ( frames )
			fclose( frames );
		if ( hits )
			fclose( hits );
		printf( "{\"seed\":%llu,\"steps\":%d,\"leaderChanges\":%d,\"hash\":\"%016llx\",\"order\":[", (unsigned long long)seed,
				r.steps, r.leaderChanges, (unsigned long long)r.hash );
		for ( int i = 0; i < racerCount; i++ )
		{
			Racer* x = racers + r.order[i];
			printf( "%s{\"name\":\"%s\",\"finished\":%s,\"time\":%.4f}", i ? "," : "", x->name,
					x->finished ? "true" : "false", x->finished ? x->finishTime : 0.0 );
		}
		printf( "]}\n" );
	}
	else if ( strcmp( argv[2], "batch" ) == 0 )
	{
		uint64_t from = strtoull( argv[3], NULL, 10 ), to = strtoull( argv[4], NULL, 10 );
		for ( uint64_t s = from; s <= to; s++ )
		{
			Result r = Run( s, NULL, NULL );
			printf( "%llu,%016llx,%d,%d", (unsigned long long)s, (unsigned long long)r.hash, r.steps, r.leaderChanges );
			for ( int i = 0; i < racerCount; i++ )
			{
				Racer* x = racers + r.order[i];
				printf( ",%s:%.4f", x->name, x->finished ? x->finishTime : -1.0 );
			}
			printf( "\n" );
		}
	}
	else
		Fail( "unknown mode" );
	return 0;
}
~~~~

## sim/build-scene.ts

~~~~ts
// Turns a trial spec and the League roster into a scene:
//   scene.json  full geometry for the renderer
//   scene.txt   flat lines for the Box2D simulator (sim/league.c)
// Usage: bun sim/build-scene.ts trials/<id>.json out/<id>
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const [specPath, outDir] = process.argv.slice(2);
if (!specPath || !outDir) throw new Error("usage: bun sim/build-scene.ts <spec.json> <outDir>");
const root = join(import.meta.dir, "..");
const spec = JSON.parse(readFileSync(specPath, "utf8"));
const roster = JSON.parse(readFileSync(join(root, "league/roster.json"), "utf8"));

type P = [number, number];
const t = spec.track;
const W = t.width, gap = t.gap, tan = Math.tan((t.angle * Math.PI) / 180);
const segs: { a: P; b: P; kind: string; friction: number; restitution: number }[] = [];
const pegs: { c: P; r: number }[] = [];
const levels: { y0: number; y1: number; dir: number; feature: string; x0: number; x1: number }[] = [];
let gate: { a: P; b: P; open: number } | null = null;
let finish: { x: number; y0: number; y1: number; dir: number } | null = null;
const slots: P[] = [];

const track = (a: P, b: P) => segs.push({ a, b, kind: "track", friction: t.friction, restitution: t.restitution });

let yStart = 0;
spec.levels.forEach((lv: any, k: number) => {
  const dir = k % 2 === 0 ? 1 : -1;
  const g = lv.gap ?? gap; // a narrower gap makes a pinch where the pack queues
  const x0 = dir > 0 ? 0 : W, x1 = dir > 0 ? W - g : g;
  const len = W - g;
  const yAt = (s: number) => yStart - s * tan; // s: distance from the wall end
  const X = (s: number) => x0 + dir * s;
  const pts: P[] = [];
  if (lv.feature === "chute") {
    // a steeper middle section: speed, and the order shuffles where it ends
    const tan2 = Math.tan((lv.angle * Math.PI) / 180), a = len * 0.3, b = len * 0.7;
    const yb = yAt(a) - (b - a) * tan2;
    pts.push([X(0), yAt(0)], [X(a), yAt(a)], [X(b), yb], [X(len), yb - (len - b) * tan]);
  } else if (lv.feature === "steps") {
    const n = lv.count, riser = 0.45, tread = len / n;
    let y = yStart;
    pts.push([X(0), y]);
    for (let i = 0; i < n; i++) {
      const ye = y - tread * tan;
      pts.push([X((i + 1) * tread), ye]);
      if (i < n - 1) pts.push([X((i + 1) * tread), ye - riser]);
      y = ye - riser;
    }
  } else {
    pts.push([X(0), yAt(0)], [X(len), yAt(len)]);
  }
  if (lv.feature === "pegs") {
    for (let i = 1; i <= lv.count; i++) {
      const s = (len * i) / (lv.count + 1);
      pegs.push({ c: [X(s), yAt(s)], r: 0.22 });
    }
  }
  for (let i = 0; i + 1 < pts.length; i++) track(pts[i], pts[i + 1]);
  const yEnd = pts[pts.length - 1][1];
  if (lv.feature === "hopper") {
    const h = spec.hopper;
    const gy = yAt(h.gateX);
    gate = { a: [h.gateX, gy], b: [h.gateX, gy + h.gateHeight], open: h.gateOpen };
    for (const r of h.rows) for (const c of h.columns) slots.push([c, yAt(c) + r]);
  }
  if (lv.feature === "finish") {
    const fx = dir > 0 ? x1 - 0.8 : x1 + 0.8;
    finish = { x: fx, y0: yEnd - 0.5, y1: yEnd + 3.5, dir };
  }
  levels.push({ y0: yStart, y1: yEnd, dir, feature: lv.feature, x0, x1 });
  yStart = yEnd - t.levelDrop;
});

const top = 7, bottom = yStart - 3.5;
segs.push({ a: [0, top], b: [0, bottom], kind: "wall", friction: 0.3, restitution: t.wallRestitution });
segs.push({ a: [W, top], b: [W, bottom], kind: "wall", friction: 0.3, restitution: t.wallRestitution });
segs.push({ a: [0, bottom], b: [W, bottom], kind: "basin", friction: 0.9, restitution: 0.0 });
if (!gate || !finish) throw new Error("spec needs a hopper level and a finish level");

// racer outlines in body coordinates, shared by simulator and renderer
const racers = roster.racers.map((r: any) => {
  let shape: any;
  if (r.kind === "circle") shape = { kind: "circle", r: r.r };
  else if (r.kind === "ngon") {
    const pts: P[] = [];
    for (let i = 0; i < r.n; i++) {
      const a = (2 * Math.PI * i) / r.n + (r.n === 4 ? Math.PI / 4 : 0);
      pts.push([+(r.r * Math.cos(a)).toFixed(5), +(r.r * Math.sin(a)).toFixed(5)]);
    }
    shape = { kind: "poly", pts };
  } else if (r.kind === "egg") {
    const pts: P[] = [];
    for (let i = 0; i < 8; i++) {
      const a = (2 * Math.PI * i) / 8;
      const y = r.b * Math.sin(a), x = r.a * Math.cos(a) * (1 - 0.18 * Math.sin(a));
      pts.push([+x.toFixed(5), +y.toFixed(5)]);
    }
    shape = { kind: "poly", pts };
  } else if (r.kind === "twin") shape = { kind: "twin", r: r.r, d: r.d };
  else if (r.kind === "capsule") shape = { kind: "capsule", half: r.half, r: r.r };
  else throw new Error(`unknown kind ${r.kind}`);
  return { ...r, shape };
});

const f = (n: number) => n.toFixed(5);
const lines: string[] = [];
lines.push(`world ${spec.world.gravity} ${spec.world.duration} ${spec.world.hz} ${spec.world.substeps}`);
lines.push(`jitter ${spec.hopper.jitter}`);
for (const s of slots) lines.push(`slot ${f(s[0])} ${f(s[1])}`);
for (const s of segs) lines.push(`seg ${f(s.a[0])} ${f(s.a[1])} ${f(s.b[0])} ${f(s.b[1])} ${s.friction} ${s.restitution}`);
for (const p of pegs) lines.push(`peg ${f(p.c[0])} ${f(p.c[1])} ${p.r} ${t.friction} ${t.restitution}`);
const g = gate as { a: P; b: P; open: number };
lines.push(`gate ${f(g.a[0])} ${f(g.a[1])} ${f(g.b[0])} ${f(g.b[1])} 0.3 0.0 ${g.open}`);
const fin = finish as { x: number; y0: number; y1: number; dir: number };
lines.push(`finish ${f(fin.x)} ${f(fin.y0)} ${f(fin.y1)} ${fin.dir}`);
for (const r of racers) {
  const s = r.shape;
  let params = "";
  if (s.kind === "circle") params = `${s.r}`;
  else if (s.kind === "poly") params = s.pts.map((p: P) => `${p[0]} ${p[1]}`).join(" ");
  else if (s.kind === "twin") params = `${s.r} ${s.d}`;
  else if (s.kind === "capsule") params = `${s.half} ${s.r}`;
  const com = r.com ? ` com ${r.com[0]} ${r.com[1]}` : "";
  lines.push(`racer ${r.name} ${s.kind} ${r.density} ${r.friction} ${r.restitution} ${r.rolling} ${params}${com}`);
}

mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "scene.txt"), lines.join("\n") + "\n");
writeFileSync(
  join(outDir, "scene.json"),
  JSON.stringify({ spec, racers, segs, pegs, gate, finish, levels, slots, bounds: { top, bottom, width: W } }, null, 1),
);
console.log(`${outDir}: ${segs.length} segments, ${pegs.length} pegs, ${levels.length} levels, bottom ${bottom.toFixed(2)} m`);
~~~~

## sim/events.ts

~~~~ts
// Event sheet of one run: what the narrator and captions may talk about.
// Everything here is read from the simulator log; nothing is added by hand.
// Usage: bun sim/events.ts <outDir> <seed>  -> <outDir>/events-<seed>.json
import { readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const [dir, seed] = process.argv.slice(2);
const scene = JSON.parse(readFileSync(join(dir, "scene.json"), "utf8"));
const result = JSON.parse(readFileSync(join(dir, `result-${seed}.json`), "utf8"));
const raw = readFileSync(join(dir, `frames-${seed}.bin`));
const [N, HZ, STEPS] = new Int32Array(raw.buffer, raw.byteOffset, 3);
const pos = new Float32Array(raw.buffer.slice(raw.byteOffset + 12, raw.byteOffset + 12 + STEPS * N * 12));
const y = (f: number, i: number) => pos[(f * N + i) * 3 + 1];
const names: string[] = scene.racers.map((r: any) => r.name);
const gate = scene.gate.open;
const finish: Record<string, number> = {};
for (const o of result.order) if (o.finished) finish[o.name] = o.time;

// running order by height, finished shapes first by time (same rule as the renderer)
const orderAt = (f: number) => {
  const t = f / HZ;
  const key = (i: number) => (finish[names[i]] !== undefined && finish[names[i]] <= t ? -1e6 + finish[names[i]] : y(f, i));
  return names.map((_, i) => i).sort((a, b) => key(a) - key(b));
};
const race = (f: number) => +(f / HZ - gate).toFixed(2);

// leader changes, same rule as the simulator: a new leader must hold for 0.5 s,
// and the first leader is the one in front 1 s after the gate opens
const hold = HZ / 2, leaders: { t: number; name: string }[] = [];
let shown = -1, cand = -1, since = 0;
for (let f = 0; f < STEPS; f++) {
  const o = orderAt(f);
  if (o[0] !== cand) { cand = o[0]; since = f; }
  if (f / HZ >= gate + 1 && cand !== shown && f - since >= hold) {
    shown = cand;
    leaders.push({ t: Math.max(0, race(since)), name: names[shown] });
  }
  if (Object.keys(finish).length && f / HZ >= Math.min(...Object.values(finish))) break;
}

// order at the quarter marks of the winner's race
const winTime = result.order[0].time;
const marks = [0.25, 0.5, 0.75].map((q) => {
  const f = Math.round((gate + q * (winTime - gate)) * HZ);
  return { share: q, t: race(f), order: orderAt(f).map((i) => names[i]) };
});

// places gained from the first second after the gate to the finish
const early = orderAt(Math.round((gate + 1) * HZ)).map((i) => names[i]);
const finalOrder = result.order.map((o: any) => o.name);
const moves = names.map((n) => ({ name: n, from: early.indexOf(n) + 1, to: finalOrder.indexOf(n) + 1 }))
  .map((m) => ({ ...m, gained: m.from - m.to })).sort((a, b) => b.gained - a.gained);

const gaps = result.order.slice(1).map((o: any, k: number) => ({
  name: o.name, behind: result.order[k].name, gap: o.finished ? +(o.time - result.order[k].time).toFixed(3) : null,
}));
// how much each shape turned on its way down: total rotation from the gate to its own finish, in full turns
const turns = names.map((n, i) => {
  const end = Math.min(STEPS - 1, Math.round((finish[n] ?? Infinity) * HZ));
  let a = 0, m = 0;
  for (let f = Math.round(gate * HZ) + 1; f <= end; f++) {
    const p = ((f - 1) * N + i) * 3, q = (f * N + i) * 3;
    let d = pos[q + 2] - pos[p + 2];
    while (d > Math.PI) d -= 2 * Math.PI;
    while (d < -Math.PI) d += 2 * Math.PI;
    a += Math.abs(d); m += Math.hypot(pos[q] - pos[p], pos[q + 1] - pos[p + 1]);
  }
  return { name: n, turns: +(a / (2 * Math.PI)).toFixed(1), metres: Math.round(m) };
});
const sheet = {
  seed: result.seed, hash: result.hash,
  winner: { name: finalOrder[0], raceTime: +(winTime - gate).toFixed(3) },
  marginToSecond: +(result.order[1].time - winTime).toFixed(3),
  photoFinish: result.order[1].time - winTime < 0.1,
  leaderChanges: leaders.length - 1, leaders,
  marks, earlyOrder: early, finalOrder, gaps,
  biggestGain: moves[0], biggestLoss: moves[moves.length - 1],
  unfinished: result.order.filter((o: any) => !o.finished).map((o: any) => o.name),
  turns,
};
writeFileSync(join(dir, `events-${seed}.json`), JSON.stringify(sheet, null, 1));
console.log(JSON.stringify(sheet, null, 1));
~~~~

## sim/stats.ts

~~~~ts
// Balance report over test runs, checked against the studio rules in quality.md.
// Usage: bun sim/stats.ts <batch.csv> [--json]
import { readFileSync } from "node:fs";

const [path, flag] = process.argv.slice(2);
const runs = readFileSync(path, "utf8").trim().split("\n").map((l) => {
  const f = l.split(",");
  const order = f.slice(4).map((x) => { const [name, t] = x.split(":"); return { name, t: Number(t) }; });
  return { seed: Number(f[0]), leaderChanges: Number(f[3]), order };
});
const n = runs.length;
const names = runs[0].order.map((o) => o.name).sort();
const median = (a: number[]) => { const s = [...a].sort((x, y) => x - y); return s[Math.floor(s.length / 2)]; };
const share = (k: number) => k / n;

const wins = new Map(names.map((x) => [x, 0])), finished = new Map(names.map((x) => [x, 0]));
const margins: number[] = [];
for (const r of runs) {
  if (r.order[0].t > 0) wins.set(r.order[0].name, wins.get(r.order[0].name)! + 1);
  for (const o of r.order) if (o.t > 0) finished.set(o.name, finished.get(o.name)! + 1);
  if (r.order[1].t > 0) margins.push(r.order[1].t - r.order[0].t);
}
const lc = runs.map((r) => r.leaderChanges);
const report = {
  runs: n,
  winShare: Object.fromEntries([...wins].sort((a, b) => b[1] - a[1]).map(([k, v]) => [k, +(100 * share(v)).toFixed(1)])),
  finishShareMin: +(100 * Math.min(...[...finished.values()].map(share))).toFixed(1),
  marginMedian: +median(margins).toFixed(3),
  marginUnder1s: +(100 * margins.filter((m) => m < 1).length / margins.length).toFixed(1),
  photoFinishUnder0_1s: +(100 * margins.filter((m) => m < 0.1).length / margins.length).toFixed(1),
  leaderChangesMedian: median(lc),
  twoPlusLeaderChanges: +(100 * lc.filter((x) => x >= 2).length / n).toFixed(1),
};
const top = Math.max(...Object.values(report.winShare));
const winners1pct = Object.values(report.winShare).filter((v) => v >= 1).length;
const checks: [string, boolean][] = [
  [`no shape above 35% wins (top ${top}%)`, top <= 35],
  [`at least 8 shapes win 1% or more (${winners1pct})`, winners1pct >= 8],
  [`every shape finishes in 99% of runs (lowest ${report.finishShareMin}%)`, report.finishShareMin >= 99],
  [`winning margin under 1 s in half of runs (${report.marginUnder1s}%)`, report.marginUnder1s >= 50],
  [`2+ leader changes in half of runs (${report.twoPlusLeaderChanges}%)`, report.twoPlusLeaderChanges >= 50],
];
if (flag === "--json") console.log(JSON.stringify({ ...report, checks: Object.fromEntries(checks) }, null, 1));
else {
  console.log(`${n} runs`);
  console.log("wins: " + Object.entries(report.winShare).map(([k, v]) => `${k} ${v}%`).join(", "));
  console.log(`winning margin median ${report.marginMedian} s; under 1 s ${report.marginUnder1s}%; under 0.1 s ${report.photoFinishUnder0_1s}%`);
  console.log(`leader changes median ${report.leaderChangesMedian}`);
  for (const [label, ok] of checks) console.log(`${ok ? "PASS" : "FAIL"}  ${label}`);
}
~~~~

## render/branding.ts

~~~~ts
// Channel branding from the approved League mockup: avatar, banner, watermark.
// One drawing per item, written twice: PNG to upload and SVG to edit (text stays text).
// Usage: bun render/branding.ts <scene.json> <outDir>
import { createCanvas, SvgExportFlag, type SKRSContext2D } from "@napi-rs/canvas";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { C, drawShape, shapeSize } from "./style";

const [scenePath, out] = process.argv.slice(2);
mkdirSync(out, { recursive: true });
const racers: any[] = JSON.parse(readFileSync(scenePath, "utf8")).racers;
const byName = (n: string) => racers.find((r) => r.name === n);

// banner: 2560×1440 as YouTube recommends; text and shapes stay inside the safe area
// (1235×338 at the 2048×1152 minimum, so 1544×422 here, centred)
const BW = 2560, BH = 1440, SW = 1544, SH = 422, SX = (BW - SW) / 2, SY = (BH - SH) / 2;
function banner(ctx: SKRSContext2D) {
  ctx.fillStyle = C.bg; ctx.fillRect(0, 0, BW, BH);
  // the start floor, then the first slope down to the right: a light surface over a dark under-fill,
  // as the track looks in the video
  const floor = SY + 404, turn = SX + SW - 60, drop = 0.42, band = 70;
  const surface = (x: number) => (x <= turn ? floor : floor + (x - turn) * drop);
  ctx.fillStyle = C.panel;
  ctx.beginPath(); ctx.moveTo(0, floor); ctx.lineTo(turn, floor); ctx.lineTo(BW, surface(BW));
  ctx.lineTo(BW, surface(BW) + band); ctx.lineTo(turn, floor + band); ctx.lineTo(0, floor + band); ctx.closePath(); ctx.fill();
  ctx.strokeStyle = C.track; ctx.lineWidth = 12; ctx.lineCap = "round";
  ctx.beginPath(); ctx.moveTo(-20, floor); ctx.lineTo(turn, floor); ctx.lineTo(BW + 20, surface(BW + 20)); ctx.stroke();
  // text block
  const x = SX + 40;
  ctx.fillStyle = C.accent; ctx.font = "32px JetBrains Mono"; ctx.fillText("SEED LOCKED · NO RETAKES", x, SY + 48);
  ctx.textAlign = "right"; ctx.fillText("SEASON 1", SX + SW - 40, SY + 48); ctx.textAlign = "left";
  ctx.fillStyle = C.text; ctx.font = "150px Barlow Condensed Bold"; ctx.fillText("SANDBOX TRIALS", x - 6, SY + 178);
  ctx.font = "56px Barlow Condensed SemiBold"; ctx.fillText("12 shapes. 8 events. One fair season.", x, SY + 244);
  // the 12 shapes waiting behind the gate, true relative sizes
  const k = 88, gap = 24;
  const widths = racers.map((r) => shapeSize(r) * 2 * k);
  let px = x + 22;
  racers.forEach((r, i) => {
    const h = (r.shape.r ?? 0.45) * k;
    drawShape(ctx, r, px + widths[i] / 2, floor - 7 - h, 0, k, false);
    px += widths[i] + gap;
  });
  ctx.strokeStyle = C.accent; ctx.lineWidth = 12; ctx.lineCap = "butt";
  ctx.beginPath(); ctx.moveTo(x, floor - 6); ctx.lineTo(x, SY + 276); ctx.lineTo(px, SY + 276); ctx.lineTo(px, floor + 34); ctx.stroke();
}

// avatar: ECHO resting at the start gate, as on the mockup; YouTube shows it as a circle at 98×98
function avatar(ctx: SKRSContext2D, size: number, plate: boolean) {
  const s = size / 100;
  if (plate) {
    ctx.fillStyle = C.bg; ctx.fillRect(0, 0, size, size);
    ctx.fillStyle = C.panel; ctx.beginPath(); ctx.arc(50 * s, 50 * s, 49 * s, 0, Math.PI * 2); ctx.fill();
  }
  const echo = byName("ECHO");
  const k = (23 * s) / echo.shape.r;
  drawShape(ctx, echo, 45 * s, 48 * s, 0.6, k, false);
  ctx.strokeStyle = C.accent; ctx.lineWidth = 9 * s; ctx.lineCap = "butt"; ctx.lineJoin = "miter";
  ctx.beginPath(); ctx.moveTo(25 * s, 75 * s); ctx.lineTo(76 * s, 75 * s); ctx.lineTo(76 * s, 38 * s); ctx.stroke();
}

const items: [string, number, number, (ctx: SKRSContext2D) => void][] = [
  ["banner-2560x1440", BW, BH, banner],
  ["avatar-800", 800, 800, (ctx) => avatar(ctx, 800, true)],
  // watermark: transparent, square, shown small in the corner of every video
  ["watermark-300", 300, 300, (ctx) => avatar(ctx, 300, false)],
];
for (const [name, w, h, draw] of items) {
  const png = createCanvas(w, h);
  draw(png.getContext("2d"));
  writeFileSync(join(out, `${name}.png`), png.encodeSync("png"));
  const svg = createCanvas(w, h, SvgExportFlag.NoPrettyXML);
  draw(svg.getContext("2d"));
  writeFileSync(join(out, `${name}.svg`), svg.getContent());
}

// checks: the banner with its safe area marked, the safe area alone (what a phone shows),
// and the avatar at the sizes YouTube shows it
const check = createCanvas(BW, BH), cc = check.getContext("2d");
banner(cc);
cc.strokeStyle = "#FF3B30"; cc.lineWidth = 6; cc.setLineDash([24, 16]); cc.strokeRect(SX, SY, SW, SH);
cc.setLineDash([]); cc.fillStyle = "#FF3B30"; cc.font = "34px JetBrains Mono";
cc.fillText("SAFE AREA 1544×422 = 1235×338 AT 2048×1152 · TEXT AND LOGO MUST STAY INSIDE", SX, SY - 22);
cc.fillText("OUTSIDE: TV ONLY", 40, 60);
writeFileSync(join(out, "check-banner-safe-area.png"), check.encodeSync("png"));
const phone = createCanvas(SW / 2, SH / 2);
phone.getContext("2d").drawImage(check, SX, SY, SW, SH, 0, 0, SW / 2, SH / 2);
writeFileSync(join(out, "check-banner-phone.png"), phone.encodeSync("png"));
const sizes = [98, 48, 24], strip = createCanvas(98 + 48 + 24 + 80, 118), sc = strip.getContext("2d");
sc.fillStyle = "#FFFFFF"; sc.fillRect(0, 0, strip.width, strip.height);
const av = createCanvas(800, 800); avatar(av.getContext("2d"), 800, true);
let ax = 10;
for (const d of sizes) {
  sc.save(); sc.beginPath(); sc.arc(ax + d / 2, 59, d / 2, 0, Math.PI * 2); sc.clip();
  sc.drawImage(av, ax, 59 - d / 2, d, d); sc.restore(); ax += d + 30;
}
writeFileSync(join(out, "check-avatar-sizes.png"), strip.encodeSync("png"));
console.log(`wrote branding to ${out}`);
~~~~

## render/cards.ts

~~~~ts
// League screens as stills: roster, rules, seed, odds, pick, results, luck or skill, table.
// Numbers come only from the test-run CSV and the official result file.
// Usage: bun render/cards.ts <outDir> <seed> <batch.csv> [--test]
//   --test marks every screen as a test run (drafts made before the official run)
import { createCanvas, loadImage, type SKRSContext2D } from "@napi-rs/canvas";
import { existsSync } from "node:fs";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { C, W, H, drawShape } from "./style";

const [dir, seedArg, batchPath, flag] = process.argv.slice(2);
const isTest = flag === "--test";
const scene = JSON.parse(readFileSync(join(dir, "scene.json"), "utf8"));
const result = JSON.parse(readFileSync(join(dir, `result-${seedArg}.json`), "utf8"));
// times shown to the millisecond: round first, so every gap on screen adds up
for (const o of result.order) o.time = Math.round(o.time * 1000) / 1000;
const racers: any[] = scene.racers;
const byName = new Map(racers.map((r) => [r.name, r]));
const spec = scene.spec;
const out = join(dir, "cards");
mkdirSync(out, { recursive: true });

// test runs: wins and finishing positions per shape
const rows = readFileSync(batchPath, "utf8").trim().split("\n").map((l) => l.split(",").slice(4).map((x) => x.split(":")[0]));
const runs = rows.length;
const wins = new Map<string, number>(), posCount = new Map<string, number[]>();
for (const r of racers) { wins.set(r.name, 0); posCount.set(r.name, Array(racers.length).fill(0)); }
for (const order of rows) order.forEach((name, k) => { if (k === 0) wins.set(name, wins.get(name)! + 1); posCount.get(name)![k]++; });

// proposed points: 12 for the winner down to 1 for 12th
const points = (place: number) => racers.length - place;
const fmt = (n: number) => n.toLocaleString("en-US");

function frame(title: string, kicker: string) {
  const canvas = createCanvas(W, H), ctx = canvas.getContext("2d");
  ctx.fillStyle = C.bg; ctx.fillRect(0, 0, W, H);
  const g = ctx.createRadialGradient(W / 2, H * 0.5, H * 0.2, W / 2, H * 0.5, H);
  g.addColorStop(0, "rgba(255,255,255,0.035)"); g.addColorStop(1, "rgba(0,0,0,0.25)");
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  ctx.fillStyle = C.accent; ctx.font = "28px JetBrains Mono"; ctx.fillText(kicker, 96, 120);
  ctx.fillStyle = C.text; ctx.font = "84px Barlow Condensed Bold"; ctx.fillText(title, 96, 205);
  ctx.font = "20px JetBrains Mono"; ctx.fillStyle = C.muted;
  ctx.fillText("GAME PHYSICS · BOX2D 3.1.1 · NOT A LAB MODEL", 96, H - 48);
  if (isTest) {
    ctx.textAlign = "right"; ctx.fillStyle = "#E5484D"; ctx.font = "26px JetBrains Mono";
    ctx.fillText(`TEST RUN · SEED ${seedArg} · NOT THE OFFICIAL RUN`, W - 96, H - 48); ctx.textAlign = "left";
  }
  return { canvas, ctx };
}
function save(name: string, canvas: any) {
  writeFileSync(join(out, `${name}.png`), canvas.encodeSync("png"));
}
function bar(ctx: SKRSContext2D, x: number, y: number, w: number, h: number, share: number, color: string) {
  ctx.fillStyle = C.panel; ctx.beginPath(); ctx.roundRect(x, y, w, h, 4); ctx.fill();
  if (share > 0) { ctx.fillStyle = color; ctx.beginPath(); ctx.roundRect(x, y, Math.max(6, w * share), h, 4); ctx.fill(); }
}
const area = (r: any) => {
  const s = r.shape;
  if (s.kind === "circle") return Math.PI * s.r * s.r;
  if (s.kind === "capsule") return Math.PI * s.r * s.r + 4 * s.half * s.r;
  if (s.kind === "twin") return 2 * Math.PI * s.r * s.r + 2 * s.d * 0.7 * s.r;
  let a = 0; const p = s.pts;
  for (let i = 0; i < p.length; i++) { const q = p[(i + 1) % p.length]; a += p[i][0] * q[1] - q[0] * p[i][1]; }
  return Math.abs(a) / 2;
};

// 1. roster
{
  const { canvas, ctx } = frame("THE LEAGUE: 12 SHAPES", `SEASON ${1} · PERMANENT ROSTER`);
  const mass = racers.map((r) => area(r) * r.density), maxLog = Math.log(Math.max(...mass) / Math.min(...mass));
  racers.forEach((r, i) => {
    const col = i % 6, row = Math.floor(i / 6);
    const x = 96 + col * 290, y = 270 + row * 370, w = 270, h = 350;
    ctx.fillStyle = C.panel; ctx.beginPath(); ctx.roundRect(x, y, w, h, 10); ctx.fill();
    ctx.fillStyle = r.color; ctx.fillRect(x, y, w, 8);
    drawShape(ctx, r, x + w / 2, y + 110, 0.35, 120, false);
    ctx.fillStyle = C.text; ctx.font = "44px Barlow Condensed Bold"; ctx.fillText(r.name, x + 20, y + 230);
    ctx.fillStyle = C.muted; ctx.font = "24px Barlow Condensed Medium"; ctx.fillText(r.tag, x + 20, y + 262);
    const stats: [string, number][] = [
      ["MASS", Math.log(mass[i] / Math.min(...mass)) / maxLog],
      ["BOUNCE", r.restitution], ["GRIP", Math.min(1, r.friction / 1.2)],
    ];
    stats.forEach(([label, v], k) => {
      ctx.fillStyle = C.muted; ctx.font = "16px JetBrains Mono"; ctx.fillText(label, x + 20, y + 292 + k * 20);
      bar(ctx, x + 100, y + 280 + k * 20, w - 120, 12, Math.max(0.02, v), r.color);
    });
  });
  save("01-roster", canvas);
}

// 2. rules
{
  const { canvas, ctx } = frame(spec.title.toUpperCase(), "TONIGHT'S RULES");
  const lines: [string, string][] = [
    ["THE QUESTION", "Which shape gets down this hill first, in our sandbox?"],
    ["START", "All 12 drop into one pile behind a gate. The gate drops at 2.0 s."],
    ["WHAT'S RANDOM", "Only the start pile. It is drawn from the locked seed."],
    ["TO WIN", "First centre across the finish line."],
    ["AT STAKE", "12 points for 1st, down to 1 point for 12th."],
  ];
  lines.forEach(([k, v], i) => {
    const y = 330 + i * 120;
    ctx.fillStyle = C.accent; ctx.font = "26px JetBrains Mono"; ctx.fillText(k, 96, y);
    ctx.fillStyle = C.text; ctx.font = "54px Barlow Condensed Medium"; ctx.fillText(v, 96, y + 58);
  });
  save("02-rules", canvas);
}

// 3. seed lock
{
  const { canvas, ctx } = frame("SEED LOCKED", "RULES FIRST. SEED LOCKED. NO RETAKES.");
  const cx = 360, cy = 560;
  ctx.strokeStyle = C.accent; ctx.lineWidth = 22;
  ctx.beginPath(); ctx.arc(cx, cy - 90, 90, Math.PI, 0); ctx.stroke();
  ctx.fillStyle = C.accent; ctx.beginPath(); ctx.roundRect(cx - 140, cy - 90, 280, 230, 18); ctx.fill();
  ctx.fillStyle = C.bg; ctx.beginPath(); ctx.arc(cx, cy, 26, 0, Math.PI * 2); ctx.fill(); ctx.fillRect(cx - 10, cy, 20, 70);
  ctx.fillStyle = C.text; ctx.font = "56px Barlow Condensed Medium";
  ctx.fillText("Track frozen before the seed was known.", 620, 420);
  ctx.fillText("Seed from a public random beacon (drand).", 620, 500);
  ctx.fillText("One official run. Rendered as it fell.", 620, 580);
  ctx.fillStyle = C.accent; ctx.font = "44px JetBrains Mono";
  ctx.fillText(isTest ? `TEST SEED ${seedArg}` : `SEED ${seedArg}`, 620, 700);
  save("03-seed", canvas);
}

// 4. odds from the test runs
{
  const { canvas, ctx } = frame("WHO USUALLY WINS?", `${fmt(runs)} TEST RUNS BEFORE THE OFFICIAL ONE`);
  const order = [...racers].sort((a, b) => wins.get(b.name)! - wins.get(a.name)!);
  const top = Math.max(...order.map((r) => wins.get(r.name)!)) / runs;
  order.forEach((r, i) => {
    const y = 270 + i * 60, share = wins.get(r.name)! / runs;
    drawShape(ctx, r, 130, y + 22, 0.2, 52, false);
    ctx.fillStyle = C.text; ctx.font = "40px Barlow Condensed SemiBold"; ctx.fillText(r.name, 190, y + 37);
    bar(ctx, 400, y + 6, 1100, 34, share / top, r.color);
    ctx.fillStyle = C.text; ctx.font = "30px JetBrains Mono";
    ctx.fillText(`${(share * 100).toFixed(1)}%  (${wins.get(r.name)})`, 1530, y + 34);
  });
  save("04-odds", canvas);
}

// 5. pick one, one screen per countdown number
for (const n of [3, 2, 1]) {
  const { canvas, ctx } = frame("PICK ONE.", "PAUSE IF YOU NEED TO");
  racers.forEach((r, i) => {
    const col = i % 6, row = Math.floor(i / 6);
    const x = 96 + col * 290 + 135, y = 420 + row * 300;
    drawShape(ctx, r, x, y, -Math.PI / 2, 190); // notch below the name
  });
  ctx.fillStyle = C.accent; ctx.font = "160px Barlow Condensed Bold"; ctx.textAlign = "right";
  ctx.fillText(String(n), W - 120, 230); ctx.textAlign = "left";
  save(`05-pick-${n}`, canvas);
}

// 6. results of this run with points
{
  const { canvas, ctx } = frame("RESULT", isTest ? "TEST RUN" : "OFFICIAL RUN");
  const order = result.order;
  const t0 = order[0].time;
  order.forEach((o: any, i: number) => {
    const col = i < 6 ? 0 : 1, row = i % 6;
    const x = 96 + col * 880, y = 260 + row * 120;
    const r = byName.get(o.name);
    ctx.fillStyle = i === 0 ? "rgba(255,201,60,0.12)" : C.panel; ctx.beginPath(); ctx.roundRect(x, y, 840, 100, 10); ctx.fill();
    ctx.fillStyle = r.color; ctx.fillRect(x, y, 10, 100);
    ctx.fillStyle = C.muted; ctx.font = "36px JetBrains Mono"; ctx.fillText(String(i + 1).padStart(2, " "), x + 30, y + 62);
    drawShape(ctx, r, x + 160, y + 50, 0.3, 70, false);
    ctx.fillStyle = C.text; ctx.font = "50px Barlow Condensed Bold"; ctx.fillText(o.name, x + 220, y + 67);
    ctx.font = "30px JetBrains Mono"; ctx.fillStyle = i === 0 ? C.accent : C.text;
    const time = o.finished ? (i === 0 ? `${(o.time - scene.gate.open).toFixed(3)} s` : `+${(o.time - t0).toFixed(3)}`) : "DNF";
    ctx.fillText(time, x + 470, y + 62);
    ctx.fillStyle = C.accent; ctx.textAlign = "right"; ctx.fillText(`${points(i)} PTS`, x + 815, y + 62); ctx.textAlign = "left";
  });
  save("06-result", canvas);
}

// 7. luck or skill: the winner's share and its finishing positions over the test runs
{
  const winner = result.order[0].name, r = byName.get(winner);
  const share = wins.get(winner)! / runs, pc = posCount.get(winner)!;
  const { canvas, ctx } = frame("LUCK OR SKILL?", "THE STATS DESK");
  drawShape(ctx, r, 260, 470, 0.3, 300);
  ctx.fillStyle = C.text; ctx.font = "64px Barlow Condensed Medium";
  ctx.fillText(`${winner} won this run.`, 520, 380);
  ctx.fillText(`In ${fmt(runs)} test runs it won ${wins.get(winner)} (${(share * 100).toFixed(1)}%).`, 520, 460);
  ctx.fillStyle = C.muted; ctx.font = "40px Barlow Condensed Medium";
  const lastTwo = pc[racers.length - 2] + pc[racers.length - 1];
  ctx.fillText(`Last two places: ${lastTwo} of ${fmt(runs)} (${(100 * lastTwo / runs).toFixed(1)}%).`, 520, 530);
  // finishing positions histogram
  const maxc = Math.max(...pc);
  ctx.font = "22px JetBrains Mono";
  pc.forEach((c, k) => {
    const x = 520 + k * 105, h = 300 * (c / maxc);
    ctx.fillStyle = k === 0 ? C.accent : r.color; ctx.globalAlpha = k === 0 ? 1 : 0.7;
    ctx.fillRect(x, 920 - h, 80, h); ctx.globalAlpha = 1;
    ctx.fillStyle = C.muted; ctx.fillText(String(k + 1), x + 30, 955);
  });
  ctx.fillStyle = C.muted; ctx.font = "24px JetBrains Mono";
  ctx.fillText(`${winner}: FINISHING PLACE IN ${fmt(runs)} TEST RUNS`, 520, 590);
  save("07-luck-or-skill", canvas);
}

// 8. season table after this event
{
  const { canvas, ctx } = frame("SEASON TABLE", "AFTER EVENT 1 OF 8");
  result.order.forEach((o: any, i: number) => {
    const r = byName.get(o.name), y = 255 + i * 62;
    ctx.fillStyle = i % 2 ? "rgba(255,255,255,0.02)" : C.panel; ctx.fillRect(96, y, 1728, 56);
    ctx.fillStyle = r.color; ctx.fillRect(96, y, 8, 56);
    ctx.fillStyle = C.muted; ctx.font = "30px JetBrains Mono"; ctx.fillText(String(i + 1).padStart(2, " "), 130, y + 39);
    ctx.fillStyle = C.text; ctx.font = "40px Barlow Condensed SemiBold"; ctx.fillText(o.name, 230, y + 42);
    ctx.fillStyle = C.accent; ctx.font = "32px JetBrains Mono"; ctx.textAlign = "right";
    ctx.fillText(String(points(i)), 1790, y + 40); ctx.textAlign = "left";
  });
  save("08-table", canvas);
}
// closest fight among the first four places: the cold open and the photo finish show it
const top4 = result.order.slice(0, 4);
let close = 1;
for (let k = 1; k < top4.length; k++) if (top4[k].time - top4[k - 1].time < top4[close].time - top4[close - 1].time) close = k;
const closeGap = top4[close].time - top4[close - 1].time;
const forWhat = close === 1 ? "FOR THE WIN" : close === 2 ? "FOR 2ND" : "FOR THE PODIUM";

// 9. cold open overlay: transparent, laid over a blurred finish
{
  const canvas = createCanvas(W, H), ctx = canvas.getContext("2d");
  ctx.fillStyle = "rgba(21,23,28,0.92)"; ctx.beginPath(); ctx.roundRect(96, H / 2 - 90, 860, 180, 10); ctx.fill();
  ctx.fillStyle = C.accent; ctx.fillRect(96, H / 2 - 90, 10, 180);
  ctx.font = "30px JetBrains Mono"; ctx.fillText("LATER IN THIS RUN", 140, H / 2 - 30);
  ctx.fillStyle = C.text; ctx.font = "72px Barlow Condensed Bold";
  ctx.fillText(`${closeGap.toFixed(3)} s ${forWhat}`, 140, H / 2 + 50);
  save("00-later", canvas);
}

// 10. photo finish: the frame where the closer of that fight crosses, with the measured gap
{
  const still = join(out, "photo-still.png");
  if (existsSync(still)) {
    const img = await loadImage(still);
    const canvas = createCanvas(W, H), ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0);
    const a = top4[close - 1], b = top4[close];
    ctx.fillStyle = "rgba(21,23,28,0.94)"; ctx.beginPath(); ctx.roundRect(W - 96 - 760, H - 330, 760, 230, 10); ctx.fill();
    ctx.fillStyle = C.accent; ctx.font = "30px JetBrains Mono"; ctx.fillText(`PHOTO FINISH · ${forWhat.replace("FOR ", "")}`, W - 820, H - 270);
    ctx.fillStyle = C.text; ctx.font = "64px Barlow Condensed Bold"; ctx.fillText(`${a.name} BY ${closeGap.toFixed(3)} s`, W - 820, H - 190);
    ctx.fillStyle = C.muted; ctx.font = "30px JetBrains Mono"; ctx.fillText(`NEXT ACROSS: ${b.name}`, W - 820, H - 135);
    save("06a-photo", canvas);
  }
  console.log(`closest top-4 fight: places ${close}-${close + 1}, ${closeGap.toFixed(3)} s; photo still time ${top4[close - 1].time.toFixed(3)} s`);
}

// 11. next event and end card
{
  const { canvas, ctx } = frame("NEXT: THE FUNNEL", "EVENT 2 OF 8");
  ctx.fillStyle = C.text; ctx.font = "56px Barlow Condensed Medium";
  ctx.fillText("12 shapes. One narrow neck. Order is everything.", 96, 420);
  ctx.fillText("Same 12 shapes. Same parameters. New arena.", 96, 500);
  save("09-next", canvas);
}
{
  const { canvas, ctx } = frame("SANDBOX TRIALS", "RULES FIRST. SEED LOCKED. NO RETAKES.");
  ctx.fillStyle = C.muted; ctx.font = "40px Barlow Condensed Medium";
  ctx.fillText("Course frozen and seed drawn in public before every official run.", 96, 330);
  save("10-end", canvas);
}
console.log(`wrote screens to ${out}`);
~~~~

## render/covers.ts

~~~~ts
// Cover options: a real frame of the official run, cropped around the shapes it is about,
// with two short lines of text. Usage: bun render/covers.ts <outDir> <seed> <episode.json>
import { createCanvas, loadImage } from "@napi-rs/canvas";
import { spawnSync } from "node:child_process";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { C } from "./style";

const [dir, seed, episodePath] = process.argv.slice(2);
const ep = JSON.parse(readFileSync(episodePath, "utf8"));
const out = join(dir, "covers");
mkdirSync(out, { recursive: true });
const CW = 1280, CH = 720;

for (const c of ep.covers) {
  const still = join(out, `frame-${c.id}.png`);
  const r = spawnSync("bun", [join(import.meta.dir, "render.ts"), dir, seed, "0", "0", still, "--png", String(c.at)],
    { stdio: "inherit", env: { ...process.env, COVER_FOCUS: c.focus.join(",") } });
  if (r.status !== 0) throw new Error("still render failed");
  const where = JSON.parse(readFileSync(still.replace(/\.png$/, ".json"), "utf8")).where;
  const pts = c.focus.map((n: string) => where[n]);
  const fx = pts.reduce((a: number, p: number[]) => a + p[0], 0) / pts.length;
  const fy = pts.reduce((a: number, p: number[]) => a + p[1], 0) / pts.length;
  // crop: the focus sits on the right third, text goes on the left
  const sw = 1920 / c.zoom, sh = sw * (CH / CW);
  const x0 = fx - sw * 0.7, y0 = fy - sh * 0.5;
  const img = await loadImage(still);
  const canvas = createCanvas(CW, CH), ctx = canvas.getContext("2d");
  ctx.fillStyle = C.bg; ctx.fillRect(0, 0, CW, CH); // a crop past the frame edge stays background
  const k = CW / sw;
  ctx.drawImage(img, -x0 * k, -y0 * k, 1920 * k, 1080 * k);
  const g = ctx.createLinearGradient(0, 0, CW * 0.65, 0);
  g.addColorStop(0, "rgba(21,23,28,0.92)"); g.addColorStop(1, "rgba(21,23,28,0)");
  ctx.fillStyle = g; ctx.fillRect(0, 0, CW, CH);
  ctx.fillStyle = C.accent; ctx.font = "150px Barlow Condensed Bold"; ctx.fillText(c.text[0], 56, 300);
  ctx.fillStyle = C.text; ctx.font = "96px Barlow Condensed Bold"; ctx.fillText(c.text[1], 60, 410);
  ctx.fillStyle = C.muted; ctx.font = "30px JetBrains Mono"; ctx.fillText("SANDBOX TRIALS · EVENT 1", 62, CH - 56);
  writeFileSync(join(out, `cover-${c.id}.png`), canvas.encodeSync("png"));
  // the same cover at phone size, to check it still reads
  const small = createCanvas(320, 180); small.getContext("2d").drawImage(canvas, 0, 0, 320, 180);
  writeFileSync(join(out, `cover-${c.id}-320.png`), small.encodeSync("png"));
}
console.log(`wrote ${ep.covers.length} covers to ${out}`);
~~~~

## render/episode.ts

~~~~ts
// Assembles a draft episode from a timeline: screens held for their line length, race segments
// rendered from the log. Picture joined without re-encoding, sound joined sample-exact and encoded once.
// Usage: bun render/episode.ts <outDir> <seed> <timeline.json> <episode.mp4> [subs-review.ass] [voice-track.json]
//   with subtitles, also writes <episode>-review.mp4: the same picture over a strip with the narration text
//   with a voice track (from render/script.ts), each line plays at its time, the sound ducks under the voice,
//   and the mix is brought to -16 LUFS in two passes
// Timeline entries: {"card": "cards/02-rules.png", "seconds": 8} or {"race": [fromSec, toSec]}
//   a race entry may add "blur": true and "overlay": "cards/x.png" (the cold open uses both),
//   and "focus": ["ANVIL", "GLIDE"] for a vertical Shorts frame with the camera on those shapes
import { spawnSync } from "node:child_process";
import { mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { basename, dirname, join, resolve } from "node:path";
import ffmpegPath from "ffmpeg-static";

const [dir, seed, timelinePath, outFile, subs, voicePath] = process.argv.slice(2);
const timeline: any[] = JSON.parse(readFileSync(timelinePath, "utf8"));
const parts = join(dirname(outFile), `parts-${basename(outFile, ".mp4")}`);
mkdirSync(parts, { recursive: true });
const ff = (args: string[]) => {
  const r = spawnSync(ffmpegPath as string, ["-y", "-loglevel", "error", ...args], { stdio: "inherit" });
  if (r.status !== 0) throw new Error(`ffmpeg failed: ${args.join(" ")}`);
};
const started = performance.now();
const list: string[] = [], sound: string[] = [];
const timing: { part: string; seconds: number; renderSeconds: number }[] = [];
timeline.forEach((e, k) => {
  const t0 = performance.now();
  const file = resolve(join(parts, `${String(k).padStart(2, "0")}.mp4`));
  if (e.card) {
    // still screen with a 0.3 s fade in and out, then quiet room tone muxed in a second pass:
    // encoding picture and sound in one FFmpeg run made it grow past 2 GB on this server
    const fade = `fade=t=in:st=0:d=0.3,fade=t=out:st=${e.seconds - 0.3}:d=0.3`;
    const silent = file.replace(/\.mp4$/, ".silent.mp4");
    // count frames, not seconds: a time trim drops the last frame and the joined episode stutters at each seam
    const frames = Math.round(e.seconds * 60);
    ff(["-i", join(dir, e.card), "-vf", `loop=loop=-1:size=1,setpts=N/60/TB,${fade},format=yuv420p`,
      "-frames:v", String(frames), "-r", "60", "-c:v", "libx264", "-preset", "medium", "-crf", "18", silent]);
    ff(["-i", silent, "-f", "lavfi", "-t", String(e.seconds), "-i", "anoisesrc=color=brown:amplitude=0.003:r=48000,aformat=channel_layouts=stereo",
      "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", file]);
    rmSync(silent);
    timing.push({ part: e.card, seconds: e.seconds, renderSeconds: (performance.now() - t0) / 1000 });
  } else if (e.race) {
    const raw = e.blur || e.overlay ? file.replace(/\.mp4$/, ".raw.mp4") : file;
    const env = e.focus ? { ...process.env, VERTICAL: e.focus.join(",") } : process.env;
    const r = spawnSync("bun", [join(import.meta.dir, "render.ts"), dir, seed, String(e.race[0]), String(e.race[1]), raw], { stdio: "inherit", env });
    if (r.status !== 0) throw new Error("race render failed");
    if (raw !== file) {
      const chain = [e.blur ? "[0:v]boxblur=12:2[b]" : "[0:v]null[b]", e.overlay ? "[b][1:v]overlay=0:0[v]" : "[b]null[v]"].join(";");
      ff(["-i", raw, ...(e.overlay ? ["-i", join(dir, e.overlay)] : []), "-filter_complex", chain, "-map", "[v]", "-map", "0:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "copy", file]);
    }
    timing.push({ part: `race ${e.race[0]}-${e.race[1]} s`, seconds: e.race[1] - e.race[0], renderSeconds: (performance.now() - t0) / 1000 });
  }
  // each part's sound cut to its exact length: joined as AAC, the encoder padding of every part
  // stays in and the sound runs late, 0.47 s by the end of the draft
  const seconds = e.card ? e.seconds : e.race[1] - e.race[0];
  const wav = file.replace(/\.mp4$/, ".wav");
  ff(["-i", file, "-map", "0:a", "-af", `atrim=duration=${seconds},apad=whole_dur=${seconds}`, "-c:a", "pcm_s16le", wav]);
  list.push(`file '${file}'`);
  sound.push(`file '${wav}'`);
});
writeFileSync(join(parts, "list.txt"), list.join("\n") + "\n");
writeFileSync(join(parts, "sound.txt"), sound.join("\n") + "\n");
const mix = join(parts, "sound.txt");
let mixArgs = ["-f", "concat", "-safe", "0", "-i", mix], chain = "alimiter=limit=0.7:level=false";
if (voicePath) {
  const lines: { file: string; at: number }[] = JSON.parse(readFileSync(voicePath, "utf8"));
  // integrated loudness of a file, EBU R128 (silence is gated out, so a voice track measures its speech)
  const loudness = (file: string) => {
    const err = spawnSync(ffmpegPath as string, ["-i", file, "-af", "loudnorm=print_format=json", "-f", "null", "-"], { encoding: "utf8" }).stderr;
    return Number(JSON.parse(err.slice(err.lastIndexOf("{"), err.lastIndexOf("}") + 1)).input_i);
  };
  // every line at its time on one track, brought to -16 LUFS as speech
  const voiceWav = join(parts, "voice.wav"), voiced = join(parts, "voiced.wav");
  const delays = lines.map((l, k) => `[${k}:a]aresample=48000,aformat=channel_layouts=stereo,adelay=${Math.round(l.at * 1000)}:all=1[v${k}]`);
  ff([...lines.flatMap((l) => ["-i", l.file]), "-filter_complex",
    [...delays, `${lines.map((_, k) => `[v${k}]`).join("")}amix=inputs=${lines.length}:normalize=0:duration=longest[out]`].join(";"),
    "-map", "[out]", "-c:a", "pcm_s24le", voiceWav]);
  const voiceGain = -16 - loudness(voiceWav);
  // the sound bed ducks under the voice, then the whole mix gets one fixed gain and a peak limiter,
  // so quiet screens are not pumped up the way a dynamic normaliser would
  ff(["-f", "concat", "-safe", "0", "-i", mix, "-i", voiceWav, "-filter_complex",
    [`[1:a]volume=${voiceGain.toFixed(2)}dB,asplit[voice][key]`, "[0:a]volume=0.7[bed]",
      "[bed][key]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=350[duck]",
      "[duck][voice]amix=inputs=2:normalize=0:duration=first[out]"].join(";"),
    "-map", "[out]", "-c:a", "pcm_s24le", voiced]);
  chain = `volume=${(-16 - loudness(voiced)).toFixed(2)}dB,alimiter=limit=0.7:level=false`;
  mixArgs = ["-i", voiced];
}
ff(["-f", "concat", "-safe", "0", "-i", join(parts, "list.txt"), ...mixArgs,
  "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", chain, "-c:a", "aac", "-b:a", "192k",
  "-movflags", "+faststart", outFile]);
if (subs) {
  const fonts = join(import.meta.dir, "..", "assets", "fonts");
  ff(["-i", outFile, "-vf", `pad=1920:1260:0:0:color=0x15171C,subtitles=filename=${subs}:fontsdir=${fonts}`,
    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart",
    outFile.replace(/\.mp4$/, "-review.mp4")]);
}
const total = (performance.now() - started) / 1000;
writeFileSync(outFile.replace(/\.mp4$/, ".timing.json"), JSON.stringify({ totalRenderSeconds: +total.toFixed(1), parts: timing }, null, 1));
console.log(`wrote ${outFile} in ${total.toFixed(1)} s`);
~~~~

## render/render.ts

~~~~ts
// Draws a simulated run frame by frame and pipes it to FFmpeg.
// Every body position comes from the simulator log; the renderer adds only
// camera, overlays and labels. Nothing in the race is animated by hand.
//
// Usage: bun render/render.ts <outDir> <seed> <fromSec> <toSec> <file.mp4> [--png <sec>]
//   VERTICAL=ANVIL,GLIDE: a 1080×1920 frame for Shorts, the camera on the named shapes
import { createCanvas, type SKRSContext2D } from "@napi-rs/canvas";
import { spawn } from "node:child_process";
import { existsSync, readFileSync, rmSync } from "node:fs";
import { join } from "node:path";
import ffmpegPath from "ffmpeg-static";
import { synthesize, writeWav } from "./sound";
import { C, W as W0, H as H0, ease, drawShape, shapeSize } from "./style";

const [dir, seedArg, fromArg, toArg, outFile, pngFlag, pngSec] = process.argv.slice(2);
const vertical = process.env.VERTICAL?.split(",");
const PPM = vertical ? 160 : 124; // pixels per metre; shapes larger on a phone
const W = vertical ? 1080 : W0, H = vertical ? 1920 : H0;
const top0 = vertical ? 300 : 172; // the arena starts below the header and the order bar

const scene = JSON.parse(readFileSync(join(dir, "scene.json"), "utf8"));
const result = JSON.parse(readFileSync(join(dir, `result-${seedArg}.json`), "utf8"));
const raw = readFileSync(join(dir, `frames-${seedArg}.bin`));
const header = new Int32Array(raw.buffer, raw.byteOffset, 3);
const [N, HZ, STEPS] = [header[0], header[1], header[2]];
const pos = new Float32Array(raw.buffer.slice(raw.byteOffset + 12, raw.byteOffset + 12 + STEPS * N * 12));
const at = (f: number, i: number) => {
  const k = (Math.min(f, STEPS - 1) * N + i) * 3;
  return [pos[k], pos[k + 1], pos[k + 2]];
};
const racers = scene.racers as any[];
const finishTime: Record<string, number> = {};
for (const r of result.order) if (r.finished) finishTime[r.name] = r.time;
const gateOpen = scene.gate.open;

// Running order: finished shapes by time, the rest by height (lower = further down the course).
// Height is averaged over 0.25 s so two shapes side by side do not swap every frame.
const SMOOTH = Math.round(0.25 * HZ);
function orderAt(f: number): number[] {
  const t = f / HZ;
  const idx = racers.map((_, i) => i);
  if (t < gateOpen + 1) return idx; // before the race: roster order
  const key = (i: number) => {
    const ft = finishTime[racers[i].name];
    if (ft !== undefined && ft <= t) return -1e6 + ft;
    let y = 0;
    for (let d = 0; d < SMOOTH; d++) y += at(Math.max(0, f - d), i)[1];
    return y / SMOOTH;
  };
  return idx.sort((a, b) => key(a) - key(b));
}

// Leader with 0.5 s hold, so a touch-and-go swap does not flash a plate.
const HOLD = Math.round(0.5 * HZ);
const leaderAt: number[] = [], orders: number[][] = [];
{
  let shown = -1, cand = -1, since = 0;
  let prev = racers.map((_, i) => i);
  for (let f = 0; f < STEPS; f++) {
    // the shown order changes only when a shape is clearly ahead (0.3 m), so chips do not flicker
    const truth = orderAt(f), rank = new Map(truth.map((i, k) => [i, k]));
    const o = [...prev];
    if (f / HZ >= gateOpen + 1) {
      const key = (i: number) => { const ft = finishTime[racers[i].name]; return ft !== undefined && ft <= f / HZ ? -1e6 + ft : at(f, i)[1]; };
      for (let pass = 0; pass < 12; pass++)
        for (let k = 0; k + 1 < o.length; k++) {
          const a = o[k], b = o[k + 1];
          const finished = key(b) < -1e5 || key(a) < -1e5;
          if ((finished && rank.get(b)! < rank.get(a)!) || (!finished && key(b) < key(a) - 0.3)) { o[k] = b; o[k + 1] = a; }
        }
    }
    prev = o;
    orders.push(o);
    // leader: same rule as the simulator and the event sheet (lowest shape, held 0.5 s)
    let low = 0;
    const lead = (i: number) => { const ft = finishTime[racers[i].name]; return ft !== undefined && ft <= f / HZ ? -1e6 + ft : at(f, i)[1]; };
    for (let i = 1; i < racers.length; i++) if (lead(i) < lead(low)) low = i;
    if (low !== cand) { cand = low; since = f; }
    if (f / HZ >= gateOpen + 1 && cand !== shown && f - since >= HOLD) shown = cand;
    leaderAt.push(f / HZ >= gateOpen + 1 ? shown : -1);
  }
}
const leaderChanges: { f: number; i: number }[] = [];
for (let f = 1; f < STEPS; f++) if (leaderAt[f] !== leaderAt[f - 1] && leaderAt[f] >= 0) leaderChanges.push({ f, i: leaderAt[f] });

// Camera: target follows the top three, then a centred Gaussian smooth (the log is known in advance).
const camTarget: number[] = [];
for (let f = 0; f < STEPS; f++) {
  const o = orders[f].filter((i) => !(finishTime[racers[i].name] <= f / HZ));
  const w = [0.5, 0.3, 0.2];
  let y = 0, s = 0;
  o.slice(0, 3).forEach((i, k) => { y += at(f, i)[1] * w[k]; s += w[k]; });
  camTarget.push(s ? y / s : camTarget[f - 1] ?? 0);
}
const SIG = 0.45 * HZ, R = Math.ceil(3 * SIG);
const camY = camTarget.map((_, f) => {
  let y = 0, s = 0;
  for (let d = -R; d <= R; d++) {
    const g = Math.exp(-(d * d) / (2 * SIG * SIG));
    y += camTarget[Math.max(0, Math.min(STEPS - 1, f + d))] * g; s += g;
  }
  return Math.min(y / s, scene.bounds.top - (H * 0.42) / PPM);
});
// covers: camera on the named shapes, and no header, bar or plates
const coverFocus = process.env.COVER_FOCUS?.split(",");
if (coverFocus) {
  const ids = coverFocus.map((n) => racers.findIndex((r) => r.name === n));
  for (let f = 0; f < STEPS; f++) camY[f] = ids.reduce((a, i) => a + at(f, i)[1], 0) / ids.length;
}
const camX = scene.bounds.width / 2;
// vertical: the camera also follows the named shapes sideways, smoothed the same way, kept near the course
const camXs = new Array(STEPS).fill(camX);
if (vertical) {
  const ids = vertical.map((n) => racers.findIndex((r) => r.name === n));
  const tx = Array.from({ length: STEPS }, (_, f) => ids.reduce((a, i) => a + at(f, i)[0], 0) / ids.length);
  const ty = Array.from({ length: STEPS }, (_, f) => ids.reduce((a, i) => a + at(f, i)[1], 0) / ids.length);
  const half = W / 2 / PPM;
  for (let f = 0; f < STEPS; f++) {
    let x = 0, y = 0, s = 0;
    for (let d = -R; d <= R; d++) {
      const g = Math.exp(-(d * d) / (2 * SIG * SIG)), k = Math.max(0, Math.min(STEPS - 1, f + d));
      x += tx[k] * g; y += ty[k] * g; s += g;
    }
    camXs[f] = Math.max(half - 0.6, Math.min(scene.bounds.width - half + 0.6, x / s));
    camY[f] = y / s;
  }
}
let camXNow = camX;
const sx = (x: number) => W / 2 + (x - camXNow) * PPM;
const sy = (y: number, f: number) => H * 0.55 - (y - camY[f]) * PPM;

function drawTrack(ctx: SKRSContext2D, f: number) {
  // under-fill gives each ramp weight; the surface line is the only bright element of the arena
  ctx.lineCap = "round"; ctx.lineJoin = "round";
  for (const s of scene.segs) {
    if (s.kind === "wall") {
      ctx.strokeStyle = C.line; ctx.lineWidth = 10;
    } else if (s.kind === "basin") {
      ctx.strokeStyle = C.line; ctx.lineWidth = 8;
    } else continue;
    ctx.beginPath(); ctx.moveTo(sx(s.a[0]), sy(s.a[1], f)); ctx.lineTo(sx(s.b[0]), sy(s.b[1], f)); ctx.stroke();
  }
  ctx.fillStyle = C.panel;
  for (const s of scene.segs) {
    if (s.kind !== "track") continue;
    ctx.beginPath();
    ctx.moveTo(sx(s.a[0]), sy(s.a[1], f)); ctx.lineTo(sx(s.b[0]), sy(s.b[1], f));
    ctx.lineTo(sx(s.b[0]), sy(s.b[1] - 0.35, f)); ctx.lineTo(sx(s.a[0]), sy(s.a[1] - 0.35, f));
    ctx.closePath(); ctx.fill();
  }
  ctx.strokeStyle = C.track; ctx.lineWidth = 7;
  for (const s of scene.segs) {
    if (s.kind !== "track") continue;
    ctx.beginPath(); ctx.moveTo(sx(s.a[0]), sy(s.a[1], f)); ctx.lineTo(sx(s.b[0]), sy(s.b[1], f)); ctx.stroke();
  }
  // section numbers on the wall side of each level
  ctx.font = "17px JetBrains Mono"; ctx.fillStyle = C.muted;
  scene.levels.forEach((lv: any, k: number) => {
    const y = sy(lv.y0 - 0.27, f);
    if (y < -40 || y > H + 40) return;
    const label = `${String(k + 1).padStart(2, "0")} ${lv.feature.toUpperCase()}`;
    ctx.save();
    ctx.translate(lv.dir > 0 ? sx(0) + 22 : sx(scene.bounds.width) - 22, y);
    ctx.rotate((lv.dir * scene.spec.track.angle * Math.PI) / 180); // along the ramp
    ctx.textAlign = lv.dir > 0 ? "left" : "right";
    ctx.fillText(label, 0, 0);
    ctx.restore();
  });
  ctx.textAlign = "left";
  // finish line
  const fin = scene.finish;
  const fy0 = sy(fin.y0, f), fy1 = sy(fin.y1, f);
  if (fy1 < H && fy0 > 0) {
    ctx.strokeStyle = C.accent; ctx.lineWidth = 4; ctx.setLineDash([14, 10]);
    ctx.beginPath(); ctx.moveTo(sx(fin.x), fy0); ctx.lineTo(sx(fin.x), fy1); ctx.stroke(); ctx.setLineDash([]);
  }
}

function drawGate(ctx: SKRSContext2D, f: number) {
  const t = f / HZ;
  const g = scene.gate;
  const fade = t < gateOpen ? 1 : 1 - (t - gateOpen) / 0.12;
  if (fade <= 0) return;
  ctx.globalAlpha = fade;
  ctx.strokeStyle = C.accent; ctx.lineWidth = 10; ctx.lineCap = "butt";
  ctx.beginPath(); ctx.moveTo(sx(g.a[0]), sy(g.a[1], f)); ctx.lineTo(sx(g.b[0]), sy(g.b[1], f)); ctx.stroke();
  ctx.globalAlpha = 1;
}

function drawBodies(ctx: SKRSContext2D, f: number, leader: number) {
  // ghost trail of the leader: last 0.6 s of the log
  if (leader >= 0) {
    const r = racers[leader];
    for (let d = 36; d > 0; d--) {
      const [x0, y0] = at(Math.max(0, f - d), leader), [x1, y1] = at(Math.max(0, f - d + 1), leader);
      ctx.strokeStyle = r.color; ctx.globalAlpha = 0.3 * (1 - d / 36); ctx.lineWidth = 0.45 * PPM * (1 - d / 40);
      ctx.lineCap = "butt";
      ctx.beginPath(); ctx.moveTo(sx(x0), sy(y0, f)); ctx.lineTo(sx(x1), sy(y1, f)); ctx.stroke();
    }
    ctx.globalAlpha = 1;
  }
  racers.forEach((r, i) => {
    const [x, y, a] = at(f, i);
    const px = sx(x), py = sy(y, f);
    if (py < -80 || py > H + 80) return;
    if (i === leader) {
      ctx.strokeStyle = C.accent; ctx.lineWidth = 5;
      ctx.beginPath(); ctx.arc(px, py, shapeSize(r) * PPM + 10, 0, Math.PI * 2); ctx.stroke();
    }
    drawShape(ctx, r, px, py, a, PPM);
  });
}

// Order bar: chips glide to their slot instead of jumping.
const chipX = racers.map(() => 0), chipY = racers.map(() => 0);
let chipInit = false;
function drawOrderBar(ctx: SKRSContext2D, f: number, leader: number) {
  const o = orders[f];
  const per = vertical ? 6 : 12, m = 48, gap = 8, cw = (W - 2 * m - gap * (per - 1)) / per, ch = 52, top = vertical ? 132 : 82;
  o.forEach((i, slot) => {
    const target = m + (slot % per) * (cw + gap), row = top + Math.floor(slot / per) * (ch + gap);
    chipX[i] = chipInit ? chipX[i] + (target - chipX[i]) * 0.25 : target;
    chipY[i] = chipInit ? chipY[i] + (row - chipY[i]) * 0.25 : row;
  });
  chipInit = true;
  racers.forEach((r, i) => {
    const x = chipX[i], top = chipY[i];
    ctx.fillStyle = C.panel; ctx.beginPath(); ctx.roundRect(x, top, cw, ch, 6); ctx.fill();
    ctx.fillStyle = r.color; ctx.fillRect(x, top, 8, ch);
    if (i === leader) { ctx.strokeStyle = C.accent; ctx.lineWidth = 3; ctx.beginPath(); ctx.roundRect(x, top, cw, ch, 6); ctx.stroke(); }
    ctx.fillStyle = C.text; ctx.font = "32px Barlow Condensed SemiBold";
    ctx.fillText(r.name, x + 20, top + 38);
  });
  // position numbers under the bar
  if (vertical) return;
  ctx.font = "18px JetBrains Mono"; ctx.fillStyle = C.muted;
  for (let s = 0; s < 12; s++) ctx.fillText(String(s + 1), m + s * (cw + gap) + 4, top + ch + 24);
}

function drawHud(ctx: SKRSContext2D, f: number) {
  const t = f / HZ;
  ctx.font = "40px Barlow Condensed Bold"; ctx.fillStyle = C.text;
  ctx.fillText("EVENT 1 · SWITCHBACK SPRINT", 48, 60);
  ctx.textAlign = "right"; ctx.font = "26px JetBrains Mono";
  const race = Math.max(0, t - gateOpen);
  const mm = Math.floor(race / 60), ss = (race % 60).toFixed(3).padStart(6, "0");
  ctx.fillStyle = C.accent; ctx.fillText(`SEED ${String(result.seed).padStart(4, "0")} · LOCKED`, W - 48, vertical ? 104 : 58);
  ctx.fillStyle = C.text; ctx.fillText(`${String(mm).padStart(2, "0")}:${ss}`, vertical ? W - 48 : W - 430, 58);
  ctx.textAlign = "left";
  ctx.font = "20px JetBrains Mono"; ctx.fillStyle = C.muted;
  // vertical: under the order bar, because the Shorts player covers the bottom of the frame
  ctx.fillText("GAME PHYSICS · BOX2D 3.1.1 · NOT A LAB MODEL", 48, vertical ? 276 : H - 36);
}

function drawRulesCard(ctx: SKRSContext2D, f: number) {
  if (vertical) return;
  const t = f / HZ;
  const a = t < 0.3 ? ease(t / 0.3) : t < gateOpen + 0.2 ? 1 : 1 - ease((t - gateOpen - 0.2) / 0.3);
  if (a <= 0) return;
  ctx.globalAlpha = a;
  const x = 48 - (1 - a) * 40, y = H - 210, w = 760, h = 132;
  ctx.fillStyle = "rgba(35,38,46,0.94)"; ctx.beginPath(); ctx.roundRect(x, y, w, h, 8); ctx.fill();
  ctx.fillStyle = C.accent; ctx.fillRect(x, y, 6, h);
  ctx.font = "24px JetBrains Mono"; ctx.fillText("RULES", x + 28, y + 40);
  ctx.fillStyle = C.text; ctx.font = "34px Barlow Condensed Medium";
  ctx.fillText("First centre across the line wins.", x + 28, y + 80);
  ctx.fillText("Start pile drawn from the locked seed.", x + 28, y + 116);
  ctx.globalAlpha = 1;
}

function drawLeaderPlate(ctx: SKRSContext2D, f: number) {
  const ch = [...leaderChanges].reverse().find((c) => c.f <= f);
  if (!ch) return;
  const age = (f - ch.f) / HZ, life = 1.8;
  if (age > life) return;
  const a = age < 0.3 ? ease(age / 0.3) : age > life - 0.3 ? 1 - ease((age - life + 0.3) / 0.3) : 1;
  const r = racers[ch.i];
  const fromLeft = sx(at(ch.f, ch.i)[0]) < W / 2;
  const w = 420, h = 108, y = vertical ? 700 : 170; // vertical: below the Shorts text box
  const x = fromLeft ? 48 - (1 - a) * (w + 60) : W - 48 - w + (1 - a) * (w + 60);
  ctx.fillStyle = "rgba(35,38,46,0.96)"; ctx.beginPath(); ctx.roundRect(x, y, w, h, 8); ctx.fill();
  ctx.fillStyle = r.color; ctx.fillRect(fromLeft ? x : x + w - 8, y, 8, h);
  ctx.fillStyle = C.accent; ctx.font = "22px JetBrains Mono";
  ctx.fillText("NEW LEADER", x + 30, y + 38);
  ctx.fillStyle = C.text; ctx.font = "54px Barlow Condensed Bold";
  ctx.fillText(r.name, x + 30, y + 92);
}

const canvas = createCanvas(W, H);
const ctx = canvas.getContext("2d");
function frame(f: number) {
  const leader = leaderAt[f];
  camXNow = camXs[Math.min(f, STEPS - 1)];
  ctx.fillStyle = C.bg; ctx.fillRect(0, 0, W, H);
  const grad = ctx.createRadialGradient(W / 2, H * 0.55, H * 0.2, W / 2, H * 0.55, H * 1.0);
  grad.addColorStop(0, "rgba(255,255,255,0.035)"); grad.addColorStop(1, "rgba(0,0,0,0.25)");
  ctx.fillStyle = grad; ctx.fillRect(0, 0, W, H);
  // the arena stays below the header, so the bar never sits on top of a shape
  if (coverFocus) { drawTrack(ctx, f); drawBodies(ctx, f, leader); return; }
  ctx.save(); ctx.beginPath(); ctx.rect(0, top0, W, H - top0); ctx.clip();
  drawTrack(ctx, f); drawGate(ctx, f); drawBodies(ctx, f, leader);
  const band = ctx.createLinearGradient(0, top0, 0, top0 + 58);
  band.addColorStop(0, "rgba(21,23,28,1)"); band.addColorStop(1, "rgba(21,23,28,0)");
  ctx.fillStyle = band; ctx.fillRect(0, top0, W, 58);
  const foot = ctx.createLinearGradient(0, H - 90, 0, H);
  foot.addColorStop(0, "rgba(21,23,28,0)"); foot.addColorStop(1, "rgba(21,23,28,0.95)");
  ctx.fillStyle = foot; ctx.fillRect(0, H - 90, W, 90);
  ctx.restore();
  drawOrderBar(ctx, f, leader); drawHud(ctx, f); drawRulesCard(ctx, f); drawLeaderPlate(ctx, f);
}

const f0 = Math.round(Number(fromArg) * HZ), f1 = Math.min(STEPS, Math.round(Number(toArg) * HZ));
if (pngFlag === "--png") {
  const target = Math.round(Number(pngSec) * HZ);
  for (let f = Math.max(0, target - 30); f <= target; f++) frame(f); // settle the chip motion
  await Bun.write(outFile, canvas.encodeSync("png"));
  // where each shape sits in the picture, so covers can crop around it
  const where = Object.fromEntries(racers.map((r, i) => { const [x, y] = at(target, i); return [r.name, [sx(x), sy(y, target)]]; }));
  await Bun.write(outFile.replace(/\.png$/, ".json"), JSON.stringify({ ppm: PPM, where }));
  console.log(`wrote ${outFile}`);
} else {
  // sound first: the whole run, then FFmpeg takes the same window as the picture
  const started = performance.now();
  const hitsPath = join(dir, `hits-${seedArg}.csv`);
  const audioArgs: string[] = [];
  if (existsSync(hitsPath)) {
    const hits = readFileSync(hitsPath, "utf8").trim().split("\n").map((l) => {
      const [st, a, b, speed, x, y] = l.split(",").map(Number);
      return { t: (st + 1) / HZ, a, b, speed, x, y };
    });
    const fr = (t: number) => Math.max(1, Math.min(STEPS - 1, Math.round(t * HZ)));
    const { L, R } = synthesize({
      seconds: STEPS / HZ + 2, hits, racers, gateOpen, camX,
      camY: (t) => camY[fr(t)],
      speeds: (t) => racers.map((_, i) => {
        const [x, y] = at(fr(t), i), [px, py] = at(fr(t) - 1, i);
        return { x, y, v: Math.hypot(x - px, y - py) * HZ };
      }),
      ticks: leaderChanges.map((c) => c.f / HZ),
      finishes: Object.values(finishTime).sort((a, b) => a - b),
    });
    const wav = join(dir, `sound-${seedArg}.wav`);
    writeWav(wav, L, R);
    audioArgs.push("-ss", String(f0 / HZ), "-t", String((f1 - f0) / HZ), "-i", wav);
  }
  // picture first into a silent file; sound is added in a second, short FFmpeg pass
  const silent = audioArgs.length ? outFile.replace(/\.mp4$/, ".silent.mp4") : outFile;
  const ff = spawn(ffmpegPath as string, [
    "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", `${W}x${H}`, "-r", String(HZ), "-i", "-",
    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", silent,
  ], { stdio: ["pipe", "inherit", "inherit"] });
  for (let f = Math.max(0, f0 - 30); f < f1; f++) {
    frame(f);
    if (f < f0) continue;
    const buf = canvas.data();
    if (!ff.stdin.write(buf)) await new Promise((res) => ff.stdin.once("drain", res));
  }
  ff.stdin.end();
  const code: number = await new Promise((res) => ff.on("close", res));
  if (code !== 0) throw new Error(`ffmpeg exited ${code}`);
  if (audioArgs.length) {
    const mux = spawn(ffmpegPath as string, [
      "-y", "-loglevel", "error", "-i", silent, ...audioArgs, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
      "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,alimiter=limit=0.75:level=false", "-ar", "48000", "-movflags", "+faststart", outFile,
    ], { stdio: ["ignore", "inherit", "inherit"] });
    const mc: number = await new Promise((res) => mux.on("close", res));
    if (mc !== 0) throw new Error(`ffmpeg mux exited ${mc}`);
    rmSync(silent);
  }
  const secs = (performance.now() - started) / 1000;
  console.log(`wrote ${outFile}: ${f1 - f0} frames in ${secs.toFixed(1)} s (${((f1 - f0) / secs).toFixed(1)} fps)`);
}
~~~~

## render/script.ts

~~~~ts
// From the episode source: the draft timeline, the script document and the ElevenLabs text.
// Screen time = the line at an even narrator pace plus a pause, never shorter than "min".
// With a voice folder from render/voice.ts, real line lengths and character timestamps replace the pace,
// a race segment grows to fit its last line, and voice-track.json says where each line plays.
// Subtitles: voice.en.srt for upload, subs-review.ass (English with the Russian line under it) for the review copy,
// drawn in a strip under the 1920×1080 picture so they never cover it.
// Usage: bun render/script.ts <episode.json> <outDir> [voiceDir]
import { readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const [episodePath, dir, voiceDir] = process.argv.slice(2);
const ep = JSON.parse(readFileSync(episodePath, "utf8"));
const wps: number = ep.wordsPerSecond;
const words = (t: string) => t.split(/\s+/).filter(Boolean).length;
const recorded = new Map<string, any>();
if (voiceDir) for (const l of JSON.parse(readFileSync(join(voiceDir, "manifest.json"), "utf8")).lines)
  recorded.set(l.text, { ...l, ...JSON.parse(readFileSync(join(voiceDir, l.file.replace(/\.mp3$/, ".json")), "utf8")) });
const say = (t: string) => recorded.get(t)?.speechSeconds ?? words(t) / wps;
const voiceTrack: { file: string; at: number }[] = [];
const tc = (s: number) => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, "0")}`;

const timeline: any[] = [];
const doc: string[] = [];
const voice: string[] = [];
let clock = 0, chars = 0, wordCount = 0, overlaps: string[] = [];
// subtitle cues: a line split at sentence ends, short sentences merged, time shared by length
const cues: { from: number; to: number; en: string; ru: string }[] = [];
const sentences = (t: string) => t.trim().split(/(?<=[.?!])\s+/).filter(Boolean);
const cue = (start: number, end: number, v: any) => {
  const en = sentences(v.text), ru = sentences(v.ru);
  if (en.length !== ru.length) throw new Error(`"${v.text}": ${en.length} English and ${ru.length} Russian sentences`);
  const chunks: { en: string; ru: string }[] = [];
  en.forEach((e, k) => {
    const last = chunks[chunks.length - 1];
    if (last && (last.en + " " + e).length <= 64) { last.en += " " + e; last.ru += " " + ru[k]; }
    else chunks.push({ en: e, ru: ru[k] });
  });
  const total = say(v.text), al = recorded.get(v.text)?.alignment;
  let t = start, at = 0;
  chunks.forEach((c, k) => {
    // recorded: the chunk runs from its first character to its last one; otherwise time is shared by length
    const from = al ? start + al.character_start_times_seconds[at] : t;
    const d = al ? al.character_end_times_seconds[at + c.en.length - 1] - al.character_start_times_seconds[at] : ((c.en.length + 1) / (v.text.length + 1)) * total;
    cues.push({ from, to: Math.min(end, from + d + (k === chunks.length - 1 ? 0.4 : 0)), en: c.en, ru: c.ru });
    t = from + d; at += c.en.length + 1;
  });
  // a cue stays up until the next one of the same line starts
  for (let k = cues.length - chunks.length; k < cues.length - 1; k++) cues[k].to = cues[k + 1].from;
  if (recorded.has(v.text)) voiceTrack.push({ file: join(voiceDir, recorded.get(v.text).file), at: +start.toFixed(3) });
};
for (const s of ep.segments) {
  let seconds: number;
  if (s.race) {
    const lastEnd = Math.max(0, ...s.voice.map((v: any) => (v.at ?? s.race[0] + 0.2) - s.race[0] + say(v.text)));
    seconds = voiceDir ? Math.max(s.race[1] - s.race[0], lastEnd + 0.4) : s.race[1] - s.race[0];
  }
  else seconds = Math.max(s.min, s.voice.reduce((a: number, v: any) => a + say(v.text) + 0.5, 0.8));
  seconds = Math.round(seconds * 10) / 10;
  timeline.push(s.race ? { race: [s.race[0], +(s.race[0] + seconds).toFixed(3)], ...(s.blur ? { blur: true } : {}), ...(s.overlay ? { overlay: s.overlay } : {}), ...(s.focus ? { focus: s.focus } : {}) } : { card: s.card, seconds });
  doc.push(`### ${tc(clock)}–${tc(clock + seconds)} · ${s.id}`, "");
  doc.push(`- Кадр: ${s.picture}`);
  if (s.learns) doc.push(`- Зритель узнаёт: ${s.learns}`);
  if (!s.voice.length) doc.push("- Голос: нет.");
  let prevEnd = -1, cardAt = 0.4;
  for (const v of s.voice) {
    if (s.race) cue(clock + (v.at ?? s.race[0] + 0.2) - s.race[0], clock + seconds, v);
    else { cue(clock + cardAt, clock + seconds, v); cardAt += say(v.text) + 0.5; }
    const at = s.race ? (v.at ?? s.race[0] + 0.2) - s.race[0] : null;
    if (at !== null && at < prevEnd) overlaps.push(`${s.id}: "${v.text}" starts before the previous line ends`);
    if (at !== null) prevEnd = at + say(v.text);
    const when = at !== null ? ` (с ${tc(clock + at)}, ${say(v.text).toFixed(1)} с)` : ` (${say(v.text).toFixed(1)} с)`;
    doc.push(`- Голос${when}: "${v.text}"`, `  - Перевод: ${v.ru}`);
    voice.push(v.text);
    chars += v.text.length; wordCount += words(v.text);
  }
  if (s.race && prevEnd > seconds) overlaps.push(`${s.id}: last line runs past the segment`);
  doc.push("");
  clock += seconds;
}
const credits = Math.ceil(chars * 1.3);
const stamp = (t: number, sep: string, cs = false) => {
  const h = Math.floor(t / 3600), m = Math.floor((t % 3600) / 60), sec = t % 60;
  const frac = cs ? Math.floor((sec % 1) * 100).toString().padStart(2, "0") : Math.floor((sec % 1) * 1000).toString().padStart(3, "0");
  return `${cs ? h : String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}:${String(Math.floor(sec)).padStart(2, "0")}${sep}${frac}`;
};
writeFileSync(join(dir, "voice.en.srt"), cues.map((c, k) => `${k + 1}\n${stamp(c.from, ",")} --> ${stamp(c.to, ",")}\n${c.en}\n`).join("\n"));
writeFileSync(join(dir, "subs-review.ass"), [
  "[Script Info]", "ScriptType: v4.00+", "PlayResX: 1920", "PlayResY: 1260", "WrapStyle: 0", "",
  "[V4+ Styles]",
  "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
  "Style: Sub,Barlow Condensed SemiBold,48,&H00F2F0EA,&H00F2F0EA,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,2,60,60,36,1",
  "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
  `Dialogue: 0,0:00:00.00,${stamp(clock, ".", true)},Sub,,0,0,0,,{\\an7\\pos(24,1094)\\fnJetBrains Mono\\fs22\\c&H0080878F&}${voiceDir ? "REVIEW COPY · NARRATION TEXT BELOW" : "REVIEW COPY · VOICE NOT RECORDED YET · NARRATION TEXT BELOW"}`,
  ...cues.map((c) => `Dialogue: 0,${stamp(c.from, ".", true)},${stamp(c.to, ".", true)},Sub,,0,0,0,,${c.en}\\N{\\fnJetBrains Mono\\fs28\\c&H00B4BEC8&}${c.ru}`),
].join("\n") + "\n");
const cps = Math.max(...cues.map((c) => c.en.length / (c.to - c.from)));
writeFileSync(join(dir, "timeline.json"), JSON.stringify(timeline, null, 1));
if (voiceDir) writeFileSync(join(dir, "voice-track.json"), JSON.stringify(voiceTrack, null, 1));
writeFileSync(join(dir, "voice.txt"), voice.join("\n\n") + "\n");
writeFileSync(join(dir, "script-body.md"), doc.join("\n"));
const summary = { cues: cues.length, maxCharsPerSecond: +cps.toFixed(1), lines: voice.length, words: wordCount, chars, creditsWith30pct: credits, voiceSeconds: +(voiceDir ? voice.reduce((a, t) => a + say(t), 0) : wordCount / wps).toFixed(1), recorded: !!voiceDir, episodeSeconds: +clock.toFixed(1), overlaps };
writeFileSync(join(dir, "script-summary.json"), JSON.stringify(summary, null, 1));
console.log(JSON.stringify(summary));
~~~~

## render/shorts.ts

~~~~ts
// Vertical Shorts from the official run: hook, race with the camera on chosen shapes, photo-finish still,
// a stats card, an end card. Every frame and number comes from the run log and the test runs.
// Usage: bun render/shorts.ts <outDir> <seed> <shorts.json> [voiceRoot]
//   writes <outDir>/shorts/<id>/<id>.mp4 (subtitles burned in), <id>.en.srt and <id>-cover.png
//   voiceRoot: folder with one render/voice.ts folder per short; without it the draft carries no voice
import { createCanvas, loadImage, type SKRSContext2D } from "@napi-rs/canvas";
import { spawnSync } from "node:child_process";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import ffmpegPath from "ffmpeg-static";
import { C } from "./style";

const [dir, seed, specPath, voiceRoot] = process.argv.slice(2);
const spec = JSON.parse(readFileSync(specPath, "utf8"));
const W = 1080, H = 1920;
const run = (cmd: string, args: string[], env = process.env) => {
  const r = spawnSync(cmd, args, { stdio: "inherit", env });
  if (r.status !== 0) throw new Error(`${cmd} failed: ${args.join(" ")}`);
};

// the text box sits just under the race header, above the shapes; the Shorts player covers the bottom
function box(ctx: SKRSContext2D, kicker: string, title: string, y = 340) {
  const lines = title.split("\n");
  const h = 90 + lines.length * 108;
  ctx.fillStyle = "rgba(35,38,46,0.94)"; ctx.beginPath(); ctx.roundRect(60, y, W - 120, h, 10); ctx.fill();
  ctx.fillStyle = C.accent; ctx.fillRect(60, y, 10, h);
  ctx.font = "30px JetBrains Mono"; ctx.fillText(kicker, 104, y + 56);
  ctx.fillStyle = C.text; ctx.font = "100px Barlow Condensed Bold";
  lines.forEach((l, k) => ctx.fillText(l, 100, y + 160 + k * 108));
}
function card(c: any) {
  const canvas = createCanvas(W, H), ctx = canvas.getContext("2d");
  ctx.fillStyle = C.bg; ctx.fillRect(0, 0, W, H);
  ctx.fillStyle = C.accent; ctx.font = "30px JetBrains Mono"; ctx.fillText(c.kicker, 80, 640);
  ctx.fillStyle = C.text; ctx.font = "124px Barlow Condensed Bold"; ctx.fillText(c.title, 76, 780);
  ctx.font = "72px Barlow Condensed Medium";
  c.lines.forEach((l: string, k: number) => ctx.fillText(l, 80, 920 + k * 96));
  ctx.fillStyle = C.muted; ctx.font = "24px JetBrains Mono";
  ctx.fillText("GAME PHYSICS · BOX2D 3.1.1 · NOT A LAB MODEL", 80, 400);
  return canvas;
}
const still = async (out: string, at: number, focus: string[]) => {
  run("bun", [join(import.meta.dir, "render.ts"), dir, seed, "0", "0", out, "--png", String(at)], { ...process.env, VERTICAL: focus.join(",") });
  return loadImage(out);
};

const stamp = (t: number) => {
  const h = Math.floor(t / 3600), m = Math.floor((t % 3600) / 60), s = t % 60;
  return `${h}:${String(m).padStart(2, "0")}:${String(Math.floor(s)).padStart(2, "0")}.${String(Math.floor((s % 1) * 100)).padStart(2, "0")}`;
};
const srtTime = (x: string) => { const [h, m, r] = x.split(":"); const [s, ms] = r.split(","); return +h * 3600 + +m * 60 + +s + +ms / 1000; };

const wps = JSON.parse(readFileSync(join(import.meta.dir, "../trials/switchback-sprint.episode.json"), "utf8")).wordsPerSecond;
for (const sh of spec.shorts) {
  const sdir = join(dir, "shorts", sh.id), rel = `shorts/${sh.id}/cards`;
  mkdirSync(join(sdir, "cards"), { recursive: true });
  const segments: any[] = [];
  let cover = "";
  for (const s of sh.segments) {
    const base = { id: s.id, voice: s.voice, picture: s.id, learns: "" };
    if (s.race) {
      let overlay;
      if (s.hook) {
        const o = createCanvas(W, H); box(o.getContext("2d"), s.hook.kicker, s.hook.title);
        writeFileSync(join(sdir, "cards", `${s.id}.png`), o.encodeSync("png"));
        overlay = `${rel}/${s.id}.png`;
        // cover: the hook over a real frame of the same moment (coverAt: a frame where the order bar is at rest)
        const frame = await still(join(sdir, "cards", `${s.id}-frame.png`), s.hook.coverAt ?? s.race[0] + 1, s.focus);
        const cv = createCanvas(W, H), cc = cv.getContext("2d");
        cc.drawImage(frame, 0, 0); cc.drawImage(o, 0, 0);
        cover = join(sdir, `${sh.id}-cover.png`);
        writeFileSync(cover, cv.encodeSync("png"));
      }
      segments.push({ ...base, race: s.race, focus: s.focus, ...(overlay ? { overlay } : {}) });
    } else if (s.still) {
      const frame = await still(join(sdir, "cards", `${s.id}-frame.png`), s.still.at, s.still.focus);
      const cv = createCanvas(W, H), cc = cv.getContext("2d");
      cc.drawImage(frame, 0, 0); box(cc, s.still.kicker, s.still.title);
      writeFileSync(join(sdir, "cards", `${s.id}.png`), cv.encodeSync("png"));
      segments.push({ ...base, card: `${rel}/${s.id}.png`, min: s.min });
    } else {
      writeFileSync(join(sdir, "cards", `${s.id}.png`), card(s.card).encodeSync("png"));
      segments.push({ ...base, card: `${rel}/${s.id}.png`, min: s.min });
    }
  }
  const epPath = join(sdir, "episode.json");
  writeFileSync(epPath, JSON.stringify({ title: sh.title, seed: +seed, wordsPerSecond: wps, segments }, null, 1));
  const voiceDir = voiceRoot ? join(voiceRoot, sh.id) : undefined;
  run("bun", [join(import.meta.dir, "script.ts"), epPath, sdir, ...(voiceDir ? [voiceDir] : [])]);
  const draft = join(sdir, `${sh.id}-nosubs.mp4`);
  run("bun", [join(import.meta.dir, "episode.ts"), dir, seed, join(sdir, "timeline.json"), draft,
    "", ...(voiceDir ? [join(sdir, "voice-track.json")] : [])]);
  // subtitles burned in, in the band above the player controls; a draft without voice says so
  const cues = readFileSync(join(sdir, "voice.en.srt"), "utf8").trim().split("\n\n").map((b) => {
    const l = b.split("\n"); const [a, z] = l[1].split(" --> ");
    return `Dialogue: 0,${stamp(srtTime(a))},${stamp(srtTime(z))},Sub,,0,0,0,,${l.slice(2).join(" ")}`;
  });
  const total = JSON.parse(readFileSync(join(sdir, "script-summary.json"), "utf8")).episodeSeconds;
  const ass = join(sdir, "subs.ass");
  writeFileSync(ass, [
    "[Script Info]", "ScriptType: v4.00+", `PlayResX: ${W}`, `PlayResY: ${H}`, "WrapStyle: 0", "",
    "[V4+ Styles]",
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
    "Style: Sub,Barlow Condensed SemiBold,66,&H00F2F0EA,&H00F2F0EA,&H30141619,&H30141619,0,0,0,0,100,100,0,0,3,14,0,2,80,170,400,1",
    "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ...(voiceDir ? [] : [`Dialogue: 0,0:00:00.00,${stamp(total)},Sub,,0,0,0,,{\\an7\\pos(48,1860)\\fnJetBrains Mono\\fs24\\bord0\\c&H0080878F&}DRAFT · VOICE NOT RECORDED YET`]),
    ...cues,
  ].join("\n") + "\n");
  const fonts = join(import.meta.dir, "..", "assets", "fonts");
  run(ffmpegPath as string, ["-y", "-loglevel", "error", "-i", draft, "-vf", `subtitles=filename=${ass}:fontsdir=${fonts}`,
    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", join(sdir, `${sh.id}.mp4`)]);
  writeFileSync(join(sdir, `${sh.id}.en.srt`), readFileSync(join(sdir, "voice.en.srt")));
  console.log(`short ${sh.id}: ${total} s, cover ${cover}`);
}
~~~~

## render/sound.ts

~~~~ts
// Sound track synthesised from the simulator log: every collision becomes a hit
// sound, moving shapes give a rolling rumble, the arena has a low room tone.
// No outside recordings, so there is nothing to license.
import { writeFileSync } from "node:fs";

export const RATE = 48000;

type Hit = { t: number; a: number; b: number; speed: number; x: number; y: number };

// deterministic noise, so the same run always gives the same sound file
function noise(seed: number) {
  let s = seed >>> 0 || 1;
  return () => {
    s ^= s << 13; s >>>= 0; s ^= s >>> 17; s ^= s << 5; s >>>= 0;
    return (s / 4294967296) * 2 - 1;
  };
}

export function synthesize(opts: {
  seconds: number; hits: Hit[]; racers: any[]; gateOpen: number; camX: number; camY: (t: number) => number;
  speeds: (t: number) => { x: number; y: number; v: number }[]; ticks: number[]; finishes: number[];
}) {
  const n = Math.ceil(opts.seconds * RATE);
  const L = new Float32Array(n), R = new Float32Array(n);
    const add = (i: number, v: number, pan: number) => {
    if (i < 0 || i >= n) return;
    L[i] += v * Math.cos(((pan + 1) * Math.PI) / 4);
    R[i] += v * Math.sin(((pan + 1) * Math.PI) / 4);
  };
  const audible = (x: number, y: number, t: number) => {
    const pan = Math.max(-1, Math.min(1, (x - opts.camX) / 8));
    const dist = Math.abs(y - opts.camY(t));
    return { pan, gain: dist < 4.5 ? 1 : Math.exp(-(dist - 4.5) / 3) };
  };

  // noise layers through a two-pole low-pass, scaled to a fixed RMS so the mix is set in dB
  const lowNoise = (hz: number, seed: number) => {
    const out = new Float32Array(n), nz = noise(seed), a = (2 * Math.PI * hz) / RATE;
    let y1 = 0, y2 = 0, sum = 0;
    for (let i = 0; i < n; i++) { y1 += a * (nz() - y1); y2 += a * (y1 - y2); out[i] = y2; sum += y2 * y2; }
    const rms = Math.sqrt(sum / n) || 1;
    for (let i = 0; i < n; i++) out[i] /= rms;
    return out;
  };
  const dB = (x: number) => Math.pow(10, x / 20);

  // room tone: about -50 dBFS
  const room = lowNoise(90, 12345);
  for (let i = 0; i < n; i++) { L[i] += room[i] * dB(-50); R[i] += room[i] * dB(-50); }

  // rolling rumble: follows the summed speed of shapes on screen, up to about -30 dBFS
  const rumble = lowNoise(180, 999);
  const block = RATE / 60;
  let level = 0, target = 0;
  for (let i = 0; i < n; i++) {
    const t = i / RATE;
    if (i % block === 0) {
      let s = 0;
      for (const b of opts.speeds(t)) s += Math.min(b.v, 8) * audible(b.x, b.y, t).gain;
      target = Math.min(1, s / 40);
    }
    level += (target - level) * 0.001;
    const v = rumble[i] * level * dB(-30);
    L[i] += v; R[i] += v;
  }

  // collisions
  for (const h of opts.hits) {
    const { pan, gain } = audible(h.x, h.y, h.t);
    if (gain < 0.05) continue;
    const loud = Math.pow(Math.min(h.speed / 7, 1), 0.8) * gain;
    const r = opts.racers[(h.a || h.b) - 1];
    const size = (r.shape.r ?? 0.45) + (r.shape.half ?? 0) * 0.5;
    const metal = r.name === "ANVIL";
    const bodyOnBody = h.a > 0 && h.b > 0;
    const f0 = (bodyOnBody ? 1300 : 420) * Math.pow(0.45 / size, 0.7) * (metal ? 0.8 : 1);
    const partials = metal ? [1, 2.76, 5.4] : [1, 2.1];
    const decay = metal ? 0.25 : bodyOnBody ? 0.035 : 0.06;
    const start = Math.round(h.t * RATE), len = Math.round(decay * 5 * RATE);
    const nz = noise(start + h.a * 31 + h.b);
    for (let k = 0; k < len; k++) {
      const tt = k / RATE, env = Math.exp(-tt / decay);
      let v = 0;
      partials.forEach((p, j) => (v += Math.sin(2 * Math.PI * f0 * p * tt) / (j + 1)));
      v = v * 0.5 + nz() * Math.exp(-tt / 0.004) * 0.6; // click transient
      add(start + k, v * env * loud * 0.5, pan);
    }
  }

  // gate drop: low clank
  {
    const start = Math.round(opts.gateOpen * RATE), nz = noise(7);
    for (let k = 0; k < RATE * 0.6; k++) {
      const tt = k / RATE;
      const v = (Math.sin(2 * Math.PI * 110 * tt) + 0.6 * Math.sin(2 * Math.PI * 293 * tt) + nz() * Math.exp(-tt / 0.01)) * Math.exp(-tt / 0.12);
      add(start + k, v * 0.35, -0.6);
    }
  }
  // soft tick when a new leader plate appears, short beep per finisher
  const tone = (t: number, f: number, dur: number, gain: number) => {
    const start = Math.round(t * RATE);
    for (let k = 0; k < dur * RATE; k++) {
      const tt = k / RATE;
      add(start + k, Math.sin(2 * Math.PI * f * tt) * Math.min(1, tt / 0.004) * Math.exp(-tt / (dur / 3)) * gain, 0);
    }
  };
  for (const t of opts.ticks) tone(t, 1480, 0.09, 0.12);
  opts.finishes.forEach((t, k) => tone(t, k === 0 ? 1760 : 1175, k === 0 ? 0.6 : 0.15, k === 0 ? 0.25 : 0.12));

  return { L, R };
}

export function writeWav(path: string, L: Float32Array, R: Float32Array) {
  const n = L.length, buf = Buffer.alloc(44 + n * 4);
  buf.write("RIFF", 0); buf.writeUInt32LE(36 + n * 4, 4); buf.write("WAVE", 8);
  buf.write("fmt ", 12); buf.writeUInt32LE(16, 16); buf.writeUInt16LE(1, 20); buf.writeUInt16LE(2, 22);
  buf.writeUInt32LE(RATE, 24); buf.writeUInt32LE(RATE * 4, 28); buf.writeUInt16LE(4, 32); buf.writeUInt16LE(16, 34);
  buf.write("data", 36); buf.writeUInt32LE(n * 4, 40);
  let peak = 0;
  for (let i = 0; i < n; i++) peak = Math.max(peak, Math.abs(L[i]), Math.abs(R[i]));
  const k = peak > 0.89 ? 0.89 / peak : 1; // headroom; loudness is set at the mux
  for (let i = 0; i < n; i++) {
    buf.writeInt16LE(Math.round(L[i] * k * 32767), 44 + i * 4);
    buf.writeInt16LE(Math.round(R[i] * k * 32767), 46 + i * 4);
  }
  writeFileSync(path, buf);
}
~~~~

## render/style.ts

~~~~ts
// League style shared by the race renderer and the screens: palette, fonts, shapes.
import { GlobalFonts, type SKRSContext2D } from "@napi-rs/canvas";
import { join } from "node:path";

const fonts = join(import.meta.dir, "../assets/fonts");
GlobalFonts.registerFromPath(join(fonts, "BarlowCondensed-SemiBold.ttf"), "Barlow Condensed SemiBold");
GlobalFonts.registerFromPath(join(fonts, "BarlowCondensed-Bold.ttf"), "Barlow Condensed Bold");
GlobalFonts.registerFromPath(join(fonts, "BarlowCondensed-Medium.ttf"), "Barlow Condensed Medium");
GlobalFonts.registerFromPath(join(fonts, "JetBrainsMono-Variable.ttf"), "JetBrains Mono");

export const C = {
  bg: "#15171C", panel: "#23262E", line: "#353840", text: "#F4F1EA", muted: "#A5A8B0",
  accent: "#FFC93C", track: "#D8D2C4",
};
export const W = 1920, H = 1080;

export const ease = (u: number) => (u <= 0 ? 0 : u >= 1 ? 1 : 1 - Math.pow(1 - u, 3));
export const shade = (hex: string, k: number) => {
  const n = parseInt(hex.slice(1), 16);
  const c = [(n >> 16) & 255, (n >> 8) & 255, n & 255].map((v) => Math.round(v * k));
  return `rgb(${c[0]},${c[1]},${c[2]})`;
};
const luminance = (hex: string) => {
  const n = parseInt(hex.slice(1), 16);
  return (0.299 * ((n >> 16) & 255) + 0.587 * ((n >> 8) & 255) + 0.114 * (n & 255)) / 255;
};

export function bodyPath(ctx: SKRSContext2D, r: any, k: number) {
  const s = r.shape;
  ctx.beginPath();
  if (s.kind === "circle") ctx.arc(0, 0, s.r * k, 0, Math.PI * 2);
  else if (s.kind === "poly") {
    s.pts.forEach((p: number[], i: number) => (i ? ctx.lineTo(p[0] * k, -p[1] * k) : ctx.moveTo(p[0] * k, -p[1] * k)));
    ctx.closePath();
  } else if (s.kind === "capsule") {
    ctx.roundRect((-s.half - s.r) * k, -s.r * k, (s.half + s.r) * 2 * k, s.r * 2 * k, s.r * k);
  } else if (s.kind === "twin") {
    ctx.arc(-s.d * k, 0, s.r * k, 0, Math.PI * 2);
    ctx.moveTo((s.d + s.r) * k, 0);
    ctx.arc(s.d * k, 0, s.r * k, 0, Math.PI * 2);
    ctx.rect(-s.d * k, -s.r * 0.35 * k, s.d * 2 * k, s.r * 0.7 * k);
  }
}

// One shape at (px, py), k pixels per metre, rotated by angle (radians, counter-clockwise).
export function drawShape(ctx: SKRSContext2D, r: any, px: number, py: number, angle: number, k: number, label = true) {
  ctx.save(); ctx.translate(px, py); ctx.rotate(-angle);
  bodyPath(ctx, r, k);
  ctx.fillStyle = r.color; ctx.fill("nonzero");
  ctx.lineWidth = (3 * k) / 124; ctx.strokeStyle = shade(r.color, 0.45); ctx.stroke();
  // rotation notch near the rim, so rolling reads at a glance
  const s = r.shape;
  const rim = (s.kind === "twin" ? s.d : s.kind === "capsule" ? s.half + s.r * 0.4 : (s.r ?? 0.4) * 0.66) * k;
  ctx.fillStyle = shade(r.color, 0.4);
  ctx.beginPath(); ctx.arc(rim, 0, (7 * k) / 124, 0, Math.PI * 2); ctx.fill();
  if (r.com) {
    ctx.fillStyle = "#501052";
    ctx.beginPath(); ctx.arc(r.com[0] * k, -r.com[1] * k, 0.09 * k, 0, Math.PI * 2); ctx.fill();
  }
  ctx.restore();
  if (!label) return;
  // name stays upright in the middle of the body
  const size = Math.round((r.name.length > 5 ? 24 : 28) * (k / 124));
  ctx.font = `${size}px Barlow Condensed Bold`; ctx.textAlign = "center";
  ctx.fillStyle = luminance(r.color) > 0.55 ? C.bg : "#FFFFFF";
  ctx.fillText(r.name, px, py + size * 0.32);
  ctx.textAlign = "left";
}

export const shapeSize = (r: any) => (r.shape.r ?? 0.45) + (r.shape.half ?? 0) + (r.shape.d ?? 0);
~~~~

## render/voice.ts

~~~~ts
// Narrator voice from ElevenLabs, one request per script line, with character timestamps.
// Calls go only through the board's spend route for this worktree. A paid request is never retried:
// any error stops the run. A line already synthesised with the same text, voice and model is kept.
// Usage: bun render/voice.ts <episode.json> <voiceDir> [voice name or id, default Brian]
//   VOICE_URL replaces the route only for tests against a fake server.
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, join } from "node:path";
import ffmpegPath from "ffmpeg-static";

const [episodePath, dir, voiceArg = "Brian"] = process.argv.slice(2);
const model = "eleven_multilingual_v2";
const top = spawnSync("git", ["rev-parse", "--show-toplevel"], { encoding: "utf8" }).stdout.trim();
const base = process.env.VOICE_URL ?? `http://127.0.0.1:41806/spend/v1/${basename(top)}/voice/elevenlabs`;
const headers = { "xi-api-key": "board-spend", "Content-Type": "application/json" };
mkdirSync(dir, { recursive: true });

const fail = async (what: string, r: Response) => {
  console.error(`${what}: HTTP ${r.status} ${(await r.text()).slice(0, 400)}`);
  process.exit(1);
};

let voiceId = voiceArg, voiceName = voiceArg;
if (!/^[A-Za-z0-9]{20}$/.test(voiceArg)) {
  const r = await fetch(`${base}/v1/voices`, { headers });
  if (!r.ok) await fail("voice list", r);
  const v = ((await r.json()).voices ?? []).find((v: any) => v.name.split(" ")[0].toLowerCase() === voiceArg.toLowerCase());
  if (!v) { console.error(`voice not found: ${voiceArg}`); process.exit(1); }
  voiceId = v.voice_id; voiceName = v.name;
}

const ep = JSON.parse(readFileSync(episodePath, "utf8"));
const lines: any[] = [];
let paidChars = 0;
for (const s of ep.segments) {
  for (const [k, v] of s.voice.entries()) {
    const id = `${s.id}-${k + 1}`;
    const key = createHash("sha256").update(`${v.text}|${voiceId}|${model}`).digest("hex").slice(0, 16);
    const mp3 = join(dir, `${id}.mp3`), meta = join(dir, `${id}.json`);
    let line = existsSync(meta) ? JSON.parse(readFileSync(meta, "utf8")) : null;
    if (line?.key !== key || !existsSync(mp3)) {
      const r = await fetch(`${base}/v1/text-to-speech/${voiceId}/with-timestamps?output_format=mp3_44100_128`,
        { method: "POST", headers, body: JSON.stringify({ text: v.text, model_id: model }) });
      if (!r.ok) await fail(`line ${id}`, r);
      const data = await r.json();
      writeFileSync(mp3, Buffer.from(data.audio_base64, "base64"));
      const al = data.alignment;
      line = { key, id, text: v.text, voiceId, model, alignment: al, speechSeconds: al.character_end_times_seconds.at(-1) };
      writeFileSync(meta, JSON.stringify(line));
      paidChars += v.text.length;
      console.log(`${id}: ${v.text.length} chars, ${line.speechSeconds.toFixed(2)} s`);
    }
    // file length, measured by decoding: the speech end above comes from the timestamps
    const probe = spawnSync(ffmpegPath as string, ["-i", mp3, "-f", "null", "-"], { encoding: "utf8" }).stderr;
    const t = [...probe.matchAll(/time=(\d+):(\d+):([\d.]+)/g)].at(-1)!;
    lines.push({ id, text: v.text, file: `${id}.mp3`, speechSeconds: line.speechSeconds, fileSeconds: +t[1] * 3600 + +t[2] * 60 + +t[3] });
  }
}
writeFileSync(join(dir, "manifest.json"), JSON.stringify({ voice: { name: voiceName, id: voiceId }, model, lines }, null, 1));
console.log(`voice ${voiceName} (${voiceId}): ${lines.length} lines, ${paidChars} characters synthesised in this run`);
~~~~

