#!/usr/bin/env node

/**
 * Copy All Vault Files to Unified Brain Structure
 */

const fs = require('fs');
const path = require('path');

const VAULTS = [
  { name: 'obsidian-mind', category: 'AI-Business' },
  { name: 'kepano-obsidian', category: 'Personal' },
  { name: 'obsidian-example-lifeos', category: 'Life-OS' },
  { name: 'ai-memory-vault', category: 'AI-Memory' },
  { name: 'obsidian-agent-vault-template', category: 'AI-Agent' },
  { name: 'agentcairn', category: 'AI-Memory' },
  { name: 'hypernovum', category: 'AI-Visualization' },
  { name: 'Obsidian-Templates', category: 'Zettelkasten' },
  { name: 'Obsidian-Zettelkasten-Starter-Kit', category: 'Zettelkasten' },
  { name: 'OB_Template', category: 'Templates' },
  { name: 'obsidian-vault-template', category: 'Templates' },
  { name: 'obsidian-n8n-bridge', category: 'n8n' },
  { name: 'ai-content-creator-toolkit', category: 'Content-Automation' },
  { name: 'obsidian_vault_template_for_researcher', category: 'Research' },
  { name: 'compass', category: 'Life-OS' },
  { name: 'NeverWrite', category: 'Agentic' },
  { name: 'technical-obsidian-template', category: 'Developer' },
  { name: 'obsidian-vault-agent', category: 'Developer-AI' },
  { name: 'obsidian-hub', category: 'Resources' },
  { name: 'Template_Hub', category: 'Templates' },
  { name: 'awesome-obsidian-vault', category: 'Resources' }
];

const CONFIG = {
  sourceDir: path.join(__dirname, '../source'),
  targetDir: path.join(__dirname, '../unified-brain'),
  dryRun: false
};

console.log('='.repeat(60));
console.log('Copying Vault Files to Unified Brain');
console.log('='.repeat(60));

let totalFiles = 0;
let totalVaults = 0;

for (const vault of VAULTS) {
  const sourcePath = path.join(CONFIG.sourceDir, vault.name);
  const targetPath = path.join(CONFIG.targetDir, vault.name);

  if (!fs.existsSync(sourcePath)) {
    console.log(`⚠️  Vault not found: ${vault.name}`);
    continue;
  }

  console.log(`\nProcessing: ${vault.name} (${vault.category})`);

  let fileCount = 0;

  function walkDir(dir, category) {
    const files = fs.readdirSync(dir);
    for (const file of files) {
      const filePath = path.join(dir, file);
      const stat = fs.statSync(filePath);

      if (stat.isDirectory()) {
        if (!file.startsWith('.') && file !== 'node_modules') {
          walkDir(filePath, category);
        }
      } else if (file.endsWith('.md')) {
        // Copy file to vault folder in target
        if (!fs.existsSync(targetPath)) {
          fs.mkdirSync(targetPath, { recursive: true });
        }
        const targetFile = path.join(targetPath, file);
        fs.copyFileSync(filePath, targetFile);
        fileCount++;
      }
    }
  }

  walkDir(sourcePath, vault.category);

  console.log(`  Files copied: ${fileCount}`);
  totalFiles += fileCount;
  totalVaults++;
}

console.log('\n' + '='.repeat(60));
console.log(`Total Vaults: ${totalVaults}`);
console.log(`Total Files: ${totalFiles}`);
console.log(`Target Directory: ${CONFIG.targetDir}`);
console.log('='.repeat(60));
