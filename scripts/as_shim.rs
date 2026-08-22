//! Minimal `as` (GNU assembler) shim for the rustup self-contained
//! windows-gnu toolchain.
//!
//! The self-contained toolchain ships `dlltool` but no real GNU `as`. When
//! rustc generates import libraries it invokes `dlltool`, which in turn spawns
//! `as` with GNU-as flags such as `--64`. The bundled `gcc` (which CAN
//! assemble) does not understand `--64` (it wants `-m64`).
//!
//! This shim translates the GNU-as-specific flags into gcc equivalents and
//! forwards everything to the bundled `x86_64-w64-mingw32-gcc.exe` in
//! assembly-input mode, producing object files exactly as a real `as` would.
//!
//! Compiled with `rustc` directly (no external deps) to avoid pulling
//! `getrandom` during the build.

use std::env;
use std::path::PathBuf;
use std::process::Command;

fn main() {
    let exe = env::current_exe().expect("current_exe");
    let dir = exe.parent().expect("parent dir");
    let gcc: PathBuf = dir.join("x86_64-w64-mingw32-gcc.exe");

    let translated: Vec<String> = env::args()
        .skip(1)
        .map(|a| match a.as_str() {
            "--64" => "-m64".to_string(),
            "--32" => "-m32".to_string(),
            "--x32" => "-mx32".to_string(),
            other => other.to_string(),
        })
        .collect();

    // Force assembly-input mode for all following inputs and compile to an
    // object file (mirrors `as` behaviour).
    let mut cmd = Command::new(&gcc);
    cmd.arg("-x").arg("assembler").arg("-c");
    cmd.args(&translated);

    let status = match cmd.status() {
        Ok(s) => s,
        Err(e) => {
            eprintln!("as-shim: failed to spawn gcc at {}: {}", gcc.display(), e);
            std::process::exit(127);
        }
    };
    std::process::exit(status.code().unwrap_or(1));
}
