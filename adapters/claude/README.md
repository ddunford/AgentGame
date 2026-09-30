# Optional Claude compatibility

CLAUDE.md forwards to the shared AGENTS.md. Existing projects that keep this
framework at `.claude/` can retain that location; other hosts are not required to.

Role files have neutral frontmatter. If the installed Claude version needs model,
memory or native agent metadata, configure that in host-local registration and
validate it against that version. No specific model family is prescribed here.

The legacy `hooks/` files contain Claude-specific event schemas, shell examples,
environment variables and `.claude/` path assumptions. They require an appropriate
Bash environment and are not portable Windows or other-host hooks. Review them
before deliberate activation; they are not installed by reading these docs.
Treat their text-pattern guards as helpers, not comprehensive enforcement.

User instructions and game scope, spend and publication policy take precedence.
The process works without hooks; never claim inactive hooks protect the project.
