import { PageFrame, PageFrameProps } from "./types"
import { FullSlug, pathToRoot, resolveRelative } from "../../util/path"

/**
 * Harbor frame: the default three-column layout plus a site-wide top bar.
 *
 * The top bar holds the brand link, the primary site navigation, and any
 * components placed in the `header` layout position (search, dark mode, ...).
 * The frame also renders its own footer (social links + back-to-top button)
 * instead of the components in the `footer` layout position.
 */
const navLinks: { label: string; slug: FullSlug; match: (slug: string) => boolean }[] = [
  { label: "Home", slug: "index" as FullSlug, match: (s) => s === "index" },
  { label: "Knowledge Base", slug: "toc" as FullSlug, match: (s) => s === "toc" },
  {
    label: "Projects",
    slug: "projects/projects-moc" as FullSlug,
    match: (s) => s.startsWith("projects/"),
  },
]

const socialLinks: { label: string; href: string }[] = [
  { label: "LinkedIn", href: "https://www.linkedin.com/in/engindenizdogu/" },
  { label: "GitHub", href: "https://github.com/engindenizdogu" },
  { label: "X", href: "https://x.com/denizdou" },
  { label: "Email", href: "mailto:edogu@stevens.edu" },
]

export const HarborFrame: PageFrame = {
  name: "harbor",
  render({
    componentData,
    header,
    beforeBody,
    pageBody: Content,
    afterBody,
    left,
    right,
  }: PageFrameProps) {
    const slug = componentData.fileData.slug!
    return (
      <>
        <div class="harbor-topbar">
          <div class="harbor-topbar-inner">
            <a class="harbor-brand" href={pathToRoot(slug)}>
              {componentData.cfg.pageTitle}
            </a>
            <nav class="harbor-nav" aria-label="Primary">
              {navLinks.map((link) => (
                <a
                  href={resolveRelative(slug, link.slug)}
                  class={link.match(slug) ? "active" : undefined}
                  aria-current={link.match(slug) ? "page" : undefined}
                >
                  {link.label}
                </a>
              ))}
            </nav>
            <div class="harbor-actions">
              {header.map((HeaderComponent) => (
                <HeaderComponent {...componentData} />
              ))}
            </div>
          </div>
        </div>
        <div class="left sidebar">
          {left.map((BodyComponent) => (
            <BodyComponent {...componentData} />
          ))}
        </div>
        <div class="center">
          <div class="page-header">
            <div class="popover-hint">
              {beforeBody.map((BodyComponent) => (
                <BodyComponent {...componentData} />
              ))}
            </div>
          </div>
          <Content {...componentData} />
          <hr />
          <div class="page-footer">
            {afterBody.map((BodyComponent) => (
              <BodyComponent {...componentData} />
            ))}
          </div>
        </div>
        <div class="right sidebar">
          {right.map((BodyComponent) => (
            <BodyComponent {...componentData} />
          ))}
        </div>
        <footer class="harbor-footer">
          <nav class="harbor-footer-links" aria-label="Social">
            {socialLinks.map((link) => (
              <a href={link.href}>{link.label}</a>
            ))}
          </nav>
          <a class="harbor-top-button" href="#quartz-root" data-no-popover="true">
            Back to top <span aria-hidden="true">↑</span>
          </a>
        </footer>
      </>
    )
  },
}
