# Wikilink Converter Plugin
#
# Purpose: Converts Obsidian-style [[wikilinks]] to proper Jekyll links at build time.
# This runs during Jekyll's rendering process, before the HTML is generated.
#
# Syntax supported:
#   [[Note Title]] -> converts to link to matching note
#   [[Display Text::https://url]] -> external link with custom text
#
# The plugin searches through all notes in the _notes collection to find matching titles.

module Jekyll
  module WikilinkConverter
    def self.convert_wikilinks(content, site)
      # Find all wikilinks in the content
      content.gsub(/\[\[([^\]]+)\]\]/) do |match|
        link_text = $1
        
        # Check if it's an external link (contains ::)
        if link_text.include?('::')
          title, url = link_text.split('::', 2)
          "<a href=\"#{url}\" target=\"_blank\" rel=\"noopener\">#{title}</a>"
        else
          # Internal link - find the matching note
          note = find_note_by_title(site, link_text)
          
          if note
            "<a href=\"#{site.baseurl}#{note.url}\" class=\"wiki-link\">#{link_text}</a>"
          else
            # Note not found - create a stale link
            "<span class=\"stale-link\" title=\"Note not found: #{link_text}\">#{link_text}</span>"
          end
        end
      end
    end
    
    def self.find_note_by_title(site, title)
      normalized_title = normalize_title(title)
      
      # Search through all notes
      site.collections['notes'].docs.find do |note|
        normalize_title(note.data['title']) == normalized_title
      end
    end
    
    def self.normalize_title(title)
      return '' unless title
      
      # Normalize smart quotes/apostrophes to straight apostrophe
      title = title.gsub(/[''`]/, "'")
      # Collapse whitespace
      title = title.gsub(/\s+/, ' ').strip
      # Case-insensitive comparison
      title.downcase
    end
  end
end

# Hook into Jekyll's rendering process
Jekyll::Hooks.register [:documents, :pages], :pre_render do |doc|
  # Only process markdown files
  if doc.extname == '.md'
    doc.content = Jekyll::WikilinkConverter.convert_wikilinks(doc.content, doc.site)
  end
end
