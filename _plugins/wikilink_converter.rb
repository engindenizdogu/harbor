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
            # Add the searched title for debugging
            Jekyll.logger.warn "Wikilink Converter:", "Could not find note: '#{link_text}'"
            "<span class=\"stale-link\" title=\"Note not found: #{link_text}\">#{link_text}</span>"
          end
        end
      end
    end
    
    def self.find_note_by_title(site, title)
      normalized_title = normalize_title(title)
      
      # Search through all notes
      notes_collection = site.collections['notes']
      return nil unless notes_collection && notes_collection.docs
      
      notes_collection.docs.find do |note|
        note_title = note.data['title']
        next unless note_title
        normalize_title(note_title) == normalized_title
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
# Use :post_read to ensure collections are loaded
Jekyll::Hooks.register :site, :post_read do |site|
  # Process all documents in the notes collection
  notes_collection = site.collections['notes']
  if notes_collection && notes_collection.docs
    notes_collection.docs.each do |doc|
      if doc.content
        doc.content = Jekyll::WikilinkConverter.convert_wikilinks(doc.content, site)
      end
    end
  end
  
  # Also process pages
  site.pages.each do |page|
    if page.content && page.path.end_with?('.md')
      page.content = Jekyll::WikilinkConverter.convert_wikilinks(page.content, site)
    end
  end
end
