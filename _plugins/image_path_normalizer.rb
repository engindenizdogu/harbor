# Image Path Normalizer Plugin
#
# Purpose: When building with GitHub Actions (not the restricted GitHub Pages build),
# this plugin rewrites root-relative image paths like:
#   <img src="/assets/img/example.png"> 
# to include the configured baseurl (e.g. "/harbor") so they work in project pages.
#
# Why: Obsidian notes often use absolute paths starting with `/assets/...` for local
# preview convenience. If the Jekyll site is published at a project subpath, those
# become broken links unless prefixed by `baseurl`.
#
# Behavior:
# - Only rewrites when `site.baseurl` is non-empty.
# - Handles <img> `src` attributes and any `srcset` entries beginning with `/assets/img/`.
# - Avoids double-prefixing when the baseurl is already present.
# - Leaves external (http/https) and protocol-relative (//) URLs untouched.
#
# Extend easily to other asset folders by adjusting the REGEX constant.

module Harbor
  class ImagePathNormalizer
    IMG_ROOT_PATTERN = %r{^/assets/img/}.freeze

    def self.normalize_src(original, baseurl)
      return original if baseurl.to_s.empty?
      return original unless original.start_with?('/')
      return original unless original =~ IMG_ROOT_PATTERN
      # Avoid double prefix if already includes baseurl
      return original if original.start_with?(baseurl + '/assets/img/')
      # Build new path and collapse potential duplicate slashes
      joined = [baseurl, original.sub(%r{^/}, '')].join('/')
      joined.gsub(%r{//+}, '/')
    end

    # Process srcset attribute: comma-separated entries with optional width descriptors
    def self.normalize_srcset(srcset_value, baseurl)
      entries = srcset_value.split(',').map(&:strip)
      normalized = entries.map do |entry|
        parts = entry.split(/\s+/)
        url = parts.shift
        url = normalize_src(url, baseurl)
        ([url] + parts).join(' ')
      end
      normalized.join(', ')
    end
  end
end

Jekyll::Hooks.register [:documents, :pages], :post_render do |doc|
  site = doc.site
  baseurl = site.config['baseurl'].to_s
  output = doc.output

  # Skip if no <img> tags or baseurl empty
  next unless output.include?('<img')

  changed = false

  # Rewrite <img ... src="/assets/img/...">
  output = output.gsub(/<img([^>]*?)src="([^"]+)"([^>]*?)>/) do |match|
    before_attrs = Regexp.last_match(1)
    src = Regexp.last_match(2)
    after_attrs = Regexp.last_match(3)
    new_src = Harbor::ImagePathNormalizer.normalize_src(src, baseurl)
    changed ||= (new_src != src)
    %Q(<img#{before_attrs}src="#{new_src}"#{after_attrs}>)
  end

  # Rewrite srcset attributes inside any tag (e.g., <img>, <source>)
  output = output.gsub(/(srcset)="([^"]+)"/) do |match|
    attr = Regexp.last_match(1)
    value = Regexp.last_match(2)
    new_value = Harbor::ImagePathNormalizer.normalize_srcset(value, baseurl)
    changed ||= (new_value != value)
    %Q(#{attr}="#{new_value}")
  end

  doc.output = output if changed
end
