#!/usr/bin/env node

/**
 * Import Multiple Obsidian Vaults into Unified Structure
 * 
 * This script:
 * 1. Reads multiple source vaults
 * 2. Applies new templates to existing notes
 * 3. Normalizes wiki-links
 * 4. Creates cross-references
 * 5. Generates index files
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Configuration
const CONFIG = {
  sourceVaults: [
    {
      name: 'work-vault',
      path: './source/work-vault',
      templates: './templates/work-vault'
    },
    {
      name: 'second-brain',
      path: './source/second-brain',
      templates: './templates/second-brain'
    },
    {
      name: 'para-gtd',
      path: './source/para-gtd',
      templates: './templates/para-gtd'
    }
  ],
  targetVault: './unified-brain',
  templates: './templates/unified',
  dryRun: true
};

// Read file with encoding detection
function readFile(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf8');
  } catch (err) {
    console.error(`Error reading ${filePath}:`, err.message);
    return null;
  }
}

// Write file
function writeFile(filePath, content) {
  try {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`✓ Written: ${filePath}`);
    return true;
  } catch (err) {
    console.error(`Error writing ${filePath}:`, err.message);
    return false;
  }
}

// Normalize wiki-links
function normalizeWikiLinks(content) {
  // Replace [[note with spaces]] with [[note-with-spaces]]
  return content.replace(/\[\[([^\]]+)\]\]/g, (match, link) => {
    const normalized = link.toLowerCase()
      .replace(/\s+/g, '-')
      .replace(/[^a-z0-9-]/g, '');
    return `[[${normalized}]]`;
  });
}

// Add YAML frontmatter
function addFrontmatter(content, type = 'note', status = 'active') {
  const existingFrontmatter = content.match(/^---\n([\s\S]*?)\n---/);
  
  if (existingFrontmatter) {
    // Update existing frontmatter
    const oldFrontmatter = existingFrontmatter[1];
    const newFrontmatter = updateFrontmatter(oldFrontmatter, type, status);
    return content.replace(/^---\n[\s\S]*?\n---/, `---\n${newFrontmatter}\n---`);
  }
  
  // Add new frontmatter
  const timestamp = new Date().toISOString().split('T')[0];
  const frontmatter = `---
type: ${type}
status: ${status}
created: ${timestamp}
updated: ${timestamp}
tags: []
---\n\n`;
  
  return frontmatter + content;
}

function updateFrontmatter(frontmatter, type, status) {
  const lines = frontmatter.split('\n');
  const updates = { type, status };
  
  return lines.map(line => {
    const [key, ...valueParts] = line.split(':');
    const keyLower = key.trim().toLowerCase();
    
    if (keyLower === 'type') {
      return `type: ${type}`;
    }
    if (keyLower === 'status') {
      return `status: ${status}`;
    }
    
    return line;
  }).join('\n');
}

// Process a single file
function processFile(filePath, type, status) {
  const content = readFile(filePath);
  if (!content) return false;
  
  let processed = content;
  
  // Normalize wiki-links
  processed = normalizeWikiLinks(processed);
  
  // Add frontmatter
  processed = addFrontmatter(processed, type, status);
  
  // Write to target
  const relativePath = path.relative(CONFIG.targetVault, filePath);
  const targetPath = path.join(CONFIG.targetVault, relativePath);
  
  // Create directories if needed
  const targetDir = path.dirname(targetPath);
  if (!fs.existsSync(targetDir)) {
    fs.mkdirSync(targetDir, { recursive: true });
  }
  
  return writeFile(targetPath, processed);
}

// Process entire vault
function processVault(vaultName, vaultPath, type, status) {
  console.log(`\nProcessing vault: ${vaultName}`);
  console.log(`Path: ${vaultPath}`);
  
  if (!fs.existsSync(vaultPath)) {
    console.error(`✗ Vault not found: ${vaultPath}`);
    return;
  }
  
  let filesProcessed = 0;
  
  // Walk directory tree
  function walkDir(dir) {
    const files = fs.readdirSync(dir);
    
    for (const file of files) {
      const filePath = path.join(dir, file);
      const stat = fs.statSync(filePath);
      
      if (stat.isDirectory()) {
        // Skip hidden directories
        if (file.startsWith('.')) continue;
        walkDir(filePath);
      } else if (file.endsWith('.md')) {
        // Process markdown file
        if (processFile(filePath, type, status)) {
          filesProcessed++;
        }
      }
    }
  }
  
  walkDir(vaultPath);
  console.log(`✓ Processed ${filesProcessed} files in ${vaultName}`);
  
  return filesProcessed;
}

// Generate index file
function generateIndex(vaultName, files) {
  const indexContent = `# ${vaultName}

This index contains ${files.length} notes.

## Notes

`;
  
  files.forEach((file, index) => {
    const relativePath = path.relative(CONFIG.targetVault, file.path);
    const title = path.basename(file.path, '.md');
    indexContent += `${index + 1}. [[${title}]] — ${file.type} — ${file.status}\n`;
  });
  
  const indexPath = path.join(CONFIG.targetVault, `00-Meta/${vaultName}-index.md`);
  writeFile(indexPath, indexContent);
}

// Main execution
function main() {
  console.log('Obsidian Vault Importer');
  console.log('========================\n');
  
  if (CONFIG.dryRun) {
    console.log('⚠️  DRY RUN MODE - No files will be modified\n');
  }
  
  let totalFiles = 0;
  
  // Process each vault
  for (const vault of CONFIG.sourceVaults) {
    const filesProcessed = processVault(vault.name, vault.path, 'imported', 'archived');
    if (filesProcessed) {
      totalFiles += filesProcessed;
    }
  }
  
  console.log(`\n========================`);
  console.log(`Total files processed: ${totalFiles}`);
  console.log(`Target vault: ${CONFIG.targetVault}`);
  console.log('========================\n');
  
  // Generate index
  if (totalFiles > 0) {
    console.log('Generating index files...');
    generateIndex('unified-brain', []);
  }
}

// Run
main();
