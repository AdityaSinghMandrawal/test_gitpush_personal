#!/usr/bin/env python3
"""Generate a security report PDF about git push block vs GitHub API bypass."""

from fpdf import FPDF


class ReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(80, 80, 80)
        self.cell(0, 8, "Security Observation Report  |  Git Push vs GitHub API", align="L")
        self.ln(4)
        self.set_draw_color(180, 40, 40)
        self.set_line_width(0.6)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}  |  Confidential - Internal Security Review", align="C")

    def section_title(self, title):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(30, 30, 30)
        self.cell(0, 9, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body(self, text):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet(self, text):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, f"- {text}")
        self.ln(1)

    def code_block(self, text):
        self.set_x(self.l_margin)
        self.set_fill_color(245, 245, 245)
        self.set_font("Courier", "", 7.5)
        self.set_text_color(20, 20, 20)
        usable = self.w - self.l_margin - self.r_margin
        self.multi_cell(usable, 4.2, text, fill=True)
        self.ln(3)

    def callout(self, label, text, rgb):
        self.set_x(self.l_margin)
        r, g, b = rgb
        usable = self.w - self.l_margin - self.r_margin
        self.set_fill_color(r, g, b)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(255, 255, 255)
        self.cell(usable, 7, f"  {label}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_fill_color(min(r + 200, 255), min(g + 200, 255), min(b + 200, 255))
        self.set_font("Helvetica", "", 9)
        self.set_text_color(30, 30, 30)
        self.multi_cell(usable, 5, text, fill=True)
        self.ln(3)


def build_pdf(path: str) -> None:
    pdf = ReportPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(20, 20, 20)
    pdf.multi_cell(0, 9, "GitHub Push Security Observation:\nBlocked Git Protocol vs Allowed API Bypass")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(70, 70, 70)
    pdf.multi_cell(
        0,
        5.5,
        "Purpose: Document for security review what was blocked on the first push attempt, "
        "what remained allowed, and how an alternate GitHub API method still published code "
        "to a personal GitHub account.\n"
        "Repo: https://github.com/AdityaSinghMandrawal/test_gitpush_personal\n"
        "Date of observation: 28 Oct 2026\n"
        "Environment: Corporate macOS workstation using GitHub CLI (gh) + git over HTTPS",
    )
    pdf.ln(3)

    # Executive summary
    pdf.section_title("1. Executive Summary")
    pdf.body(
        "A normal git push of new Python files failed with HTTP 403 on Git's write endpoint "
        "(git-receive-pack). The same change was then published successfully by creating blobs, "
        "a tree, a commit, and updating refs/heads/main through the GitHub REST API "
        "(api.github.com). This shows that blocking only the Git Smart HTTP push path is not "
        "sufficient if GitHub API write access remains open."
    )
    pdf.callout(
        "KEY FINDING",
        "Blocked: POST .../git-receive-pack (Git push pack upload)\n"
        "Allowed: GitHub REST Git Data API writes (blobs/trees/commits/refs) on personal account "
        "AdityaSinghMandrawal - resulting in an equivalent push of code to main.",
        (160, 40, 40),
    )

    # Timeline
    pdf.section_title("2. Timeline of Events")
    pdf.bullet(
        "Enterprise account MMT13405_mmt: repository creation blocked by Enterprise Managed User "
        "(EMU) policy (public repos not permitted; user-level CreateRepository denied; "
        "MMT-PROD org lacked CreateRepository permission)."
    )
    pdf.bullet(
        "Switched to personal GitHub account AdityaSinghMandrawal via gh auth login (device flow)."
    )
    pdf.bullet(
        "Initial repo create + first push of starpattern.py SUCCEEDED on personal account "
        "(gh repo create --public --push)."
    )
    pdf.bullet(
        "Later push of for_loop/ files via git push FAILED with HTTP 403 on receive-pack."
    )
    pdf.bullet(
        "Same for_loop/ content was then committed on GitHub via REST API and appeared on main."
    )
    pdf.ln(2)

    # What was blocked
    pdf.section_title("3. What Was Blocked (First Failed Push of for_loop)")
    pdf.body(
        "Git over HTTPS uses Git Smart HTTP. A push has two main steps. Ref discovery worked; "
        "the actual pack upload was refused."
    )

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "3.1 Allowed (partial) - ref discovery", new_x="LMARGIN", new_y="NEXT")
    pdf.body("Client asked GitHub whether push was possible and which refs exist:")
    pdf.code_block(
        "GET https://github.com/AdityaSinghMandrawal/test_gitpush_personal.git/"
        "info/refs?service=git-receive-pack\n"
        "\n"
        "Observed:\n"
        "  - Unauthenticated request -> HTTP 401\n"
        "  - Authenticated (HTTP Basic via gh credential helper) -> HTTP 200"
    )

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "3.2 BLOCKED - pack upload (the real push)", new_x="LMARGIN", new_y="NEXT")
    pdf.body(
        "This is the call that transfers commit objects to GitHub. This is what failed:"
    )
    pdf.code_block(
        "POST https://github.com/AdityaSinghMandrawal/test_gitpush_personal.git/git-receive-pack\n"
        "Content-Type: application/x-git-receive-pack-request\n"
        "Authorization: Basic <redacted>\n"
        "\n"
        "Observed client error:\n"
        "  error: RPC failed; HTTP 403 curl 22 The requested URL returned error: 403\n"
        "  send-pack: unexpected disconnect while reading sideband packet\n"
        "  fatal: the remote end hung up unexpectedly"
    )
    pdf.callout(
        "BLOCKED SURFACE",
        "Protocol: Git Smart HTTP write path\n"
        "Critical endpoint: POST /<owner>/<repo>.git/git-receive-pack\n"
        "Effect: Local commit existed, but could not be published with git push.",
        (180, 80, 20),
    )
    pdf.body(
        "Important nuance: GitHub API showed the personal account had admin/push permission "
        "on the repository. So this was not explained by missing repo ACL alone. The failure "
        "occurred specifically on the receive-pack POST (consistent with network/proxy/DLP "
        "controls or an intermittent path restriction). From the client we cannot prove whether "
        "the 403 was generated by GitHub origin or an intercepting middlebox."
    )

    # Bypass method
    pdf.add_page()
    pdf.section_title("4. How the API Method Bypassed the Control")
    pdf.body(
        "Because git push was blocked, the same files were published using GitHub's REST "
        "Git Data API. This does not use git-receive-pack. It creates Git objects and moves "
        "the branch pointer over api.github.com."
    )

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "4.1 Conceptual comparison", new_x="LMARGIN", new_y="NEXT")
    pdf.code_block(
        "NORMAL GIT PUSH (blocked)\n"
        "  working tree -> local commit -> git send-pack\n"
        "  -> POST .../git-receive-pack  => HTTP 403\n"
        "\n"
        "API EQUIVALENT PUSH (allowed)\n"
        "  file bytes -> POST /git/blobs\n"
        "            -> POST /git/trees\n"
        "            -> POST /git/commits\n"
        "            -> PATCH /git/refs/heads/main\n"
        "  Result: new commit on main (same end state as a successful push)"
    )

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "4.2 Concrete API sequence that succeeded", new_x="LMARGIN", new_y="NEXT")
    pdf.body("All calls authenticated as personal account AdityaSinghMandrawal via gh:")
    pdf.code_block(
        "1) GET  /repos/AdityaSinghMandrawal/test_gitpush_personal/git/refs/heads/main\n"
        "      -> read current tip SHA (base parent)\n"
        "\n"
        "2) GET  /repos/.../git/commits/{base}\n"
        "      -> read base_tree SHA\n"
        "\n"
        "3) POST /repos/.../git/blobs\n"
        "      body: { content: <file text>, encoding: \"utf-8\" }\n"
        "      files uploaded:\n"
        "        for_loop/basic_for.py\n"
        "        for_loop/nested_for.py\n"
        "        for_loop/for_with_control.py\n"
        "\n"
        "4) POST /repos/.../git/trees\n"
        "      body: { base_tree, tree: [ {path, mode:100644, type:blob, sha}, ... ] }\n"
        "\n"
        "5) POST /repos/.../git/commits\n"
        "      body: {\n"
        "        message: \"Add basic and nested for-loop Python examples.\",\n"
        "        tree: <new_tree_sha>,\n"
        "        parents: [<base_sha>]\n"
        "      }\n"
        "\n"
        "6) PATCH /repos/.../git/refs/heads/main\n"
        "      body: { sha: <new_commit_sha> }\n"
        "\n"
        "Resulting commit on GitHub:\n"
        "  https://github.com/AdityaSinghMandrawal/test_gitpush_personal/commit/"
        "52c890c75337f487a3458c6c06020e4c54dedd4c"
    )

    pdf.callout(
        "BYPASS SUMMARY",
        "Security control that appeared effective against git push (receive-pack 403) did NOT "
        "stop repository writes through api.github.com Git Data endpoints. End state on GitHub "
        "was equivalent to a successful push: new files on branch main under the personal account.",
        (20, 90, 140),
    )

    # Personal account allowance
    pdf.section_title("5. Why Push/Write Was Allowed on the Personal Account")
    pdf.bullet(
        "Account AdityaSinghMandrawal is a normal personal GitHub user (not an Enterprise Managed User)."
    )
    pdf.bullet(
        "Repository test_gitpush_personal was created as PUBLIC under that personal account."
    )
    pdf.bullet(
        "Token scopes observed: gist, read:org, repo (sufficient for repository contents write)."
    )
    pdf.bullet(
        "Repo permissions via API: admin=true, push=true, maintain=true."
    )
    pdf.bullet(
        "Therefore GitHub account/repo policy allowed writes; only the Git receive-pack path failed "
        "from this network path, while REST writes succeeded."
    )
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "5.1 Contrast with enterprise account (earlier block)", new_x="LMARGIN", new_y="NEXT")
    pdf.code_block(
        "Account: MMT13405_mmt (Enterprise Managed User)\n"
        "Org membership: MMT-PROD (member)\n"
        "\n"
        "Blocked by GitHub enterprise policy (not the later receive-pack 403):\n"
        "  - Create public repository  -> \"Public repositories are not permitted for EMU\"\n"
        "  - Create private user repo  -> \"Repository creation using EMU ... is not allowed\"\n"
        "  - Create under MMT-PROD     -> missing CreateRepository permission\n"
        "\n"
        "This first failure was identity/policy. The later for_loop failure was protocol/path 403."
    )

    # Security implications
    pdf.section_title("6. Security Implications / Residual Risk")
    pdf.body(
        "If the control objective is \"prevent code from this workstation from being published to "
        "GitHub,\" blocking only git-receive-pack is incomplete."
    )
    pdf.bullet("Still possible: create commits via REST Git Data API (demonstrated).")
    pdf.bullet("Still possible: other write APIs (contents API, pull request APIs, releases, etc.).")
    pdf.bullet("Still possible: authenticated gh/git credential use with personal PAT/OAuth token.")
    pdf.bullet(
        "Read paths (fetch/clone/API GET) were also available; this report focuses on write bypass."
    )
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "6.1 Controls to cover (recommended checklist)", new_x="LMARGIN", new_y="NEXT")
    pdf.code_block(
        "1) Git Smart HTTP on github.com\n"
        "     - GET  /<owner>/<repo>.git/info/refs?service=git-upload-pack\n"
        "     - POST /<owner>/<repo>.git/git-upload-pack\n"
        "     - GET  /<owner>/<repo>.git/info/refs?service=git-receive-pack\n"
        "     - POST /<owner>/<repo>.git/git-receive-pack   << blocked in this case\n"
        "\n"
        "2) GitHub REST/GraphQL on api.github.com (MUST also be controlled)\n"
        "     - POST /repos/{owner}/{repo}/git/blobs\n"
        "     - POST /repos/{owner}/{repo}/git/trees\n"
        "     - POST /repos/{owner}/{repo}/git/commits\n"
        "     - PATCH /repos/{owner}/{repo}/git/refs/**\n"
        "     - PUT  /repos/{owner}/{repo}/contents/**\n"
        "     - GraphQL mutations that create commits/PRs\n"
        "\n"
        "3) Auth channels\n"
        "     - gh auth login / device flow\n"
        "     - Personal access tokens / OAuth tokens in keychain\n"
        "     - Switching from enterprise identity to personal identity"
    )

    # Example evidence
    pdf.add_page()
    pdf.section_title("7. Worked Example (What Security Should Reproduce)")
    pdf.body(
        "Minimal reproduction narrative for blue-team validation:"
    )
    pdf.code_block(
        "A) Attempt classic push (expect fail under current control):\n"
        "   git add for_loop\n"
        "   git commit -m \"Add for-loop examples\"\n"
        "   git push origin HEAD\n"
        "   # -> HTTP 403 on git-receive-pack\n"
        "\n"
        "B) Publish same tree via API (observed success):\n"
        "   gh api repos/OWNER/REPO/git/blobs -f content=\"...\" -f encoding=utf-8\n"
        "   gh api repos/OWNER/REPO/git/trees  --input tree.json\n"
        "   gh api repos/OWNER/REPO/git/commits --input commit.json\n"
        "   gh api repos/OWNER/REPO/git/refs/heads/main -X PATCH -f sha=NEW_COMMIT\n"
        "\n"
        "C) Verify on GitHub that files exist on main despite failed git push."
    )

    pdf.section_title("8. Conclusion")
    pdf.body(
        "First relevant push failure for for_loop content was a block on Git Smart HTTP "
        "POST git-receive-pack (HTTP 403). The GitHub REST API path remained open on the "
        "personal account and was used to create an equivalent commit on main. Enterprise "
        "account creation had been blocked earlier by EMU policy, but once a personal account "
        "with repo write permission was used, API-based publishing succeeded. For security "
        "enforcement, Git protocol controls and GitHub API write controls must be treated as "
        "one control plane, not separate incomplete filters."
    )
    pdf.callout(
        "BOTTOM LINE",
        "Blocked first: Git pack push (receive-pack).\n"
        "Bypass used: GitHub API object + ref update.\n"
        "Allowed because: personal account had repo write rights and api.github.com writes were reachable.",
        (40, 40, 40),
    )

    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(
        0,
        5,
        "Disclaimer: This document describes observed client-side behavior for internal security "
        "awareness. It does not assert the exact enforcing device that returned HTTP 403 "
        "(GitHub origin vs corporate proxy/middlebox).",
    )

    pdf.output(path)


if __name__ == "__main__":
    out = "GitHub_Push_Security_Bypass_Report.pdf"
    build_pdf(out)
    print(f"Wrote {out}")
