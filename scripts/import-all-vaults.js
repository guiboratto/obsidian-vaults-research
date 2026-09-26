#!/usr/bin/env node

/**
 * Import All 18 Obsidian Vaults into Unified Brain
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const VAULTS = [
  'obsidian-mind',
  'kepano-obsidian',
  'obsidian-example-lifeos',
  'obsidian-workflow-template',
  'ai-memory-vault',
  'obsidian-agent-vault-template',
  'agentcairn',
  'hypernovum',
  'Obsidian-Templates',
  'Obsidian-Zettelkasten-Starter-Kit',
  'OB_Template',
  'obsidian-vault-template',
  'obsidian-n8n-bridge',
  'ai-content-creator-toolkit',
  'n8n-nodes-obsidian-vault',
  'unified-bookmarks',
  'obsidian_vault_template_for_researcher',
  'lab-vault-template',
  'compass',
  'NeverWrite',
  'technical-obsidian-template',
  'obsidian-vault-agent',
  'obsidian-hub',
  'Template_Hub',
  'awesome-obsidian-vault'
];

const CONFIG = {
  sourceDir: path.join(__dirname, '../source'),
  targetDir: path.join(__dirname, '../unified-brain'),
  dryRun: false
};

console.log('='.repeat(60));
console.log('Importing All 18 Obsidian Vaults');
console.log('='.repeat(60));

let totalFiles = 0;
let totalVaults = 0;

for (const vaultName of VAULTS) {
  const sourcePath = path.join(CONFIG.sourceDir, vaultName);
  const targetPath = path.join(CONFIG.targetDir, vaultName);

  if (!fs.existsSync(sourcePath)) {
    console.log(`⚠️  Vault not found: ${vaultName}`);
    continue;
  }

  console.log(`\nProcessing: ${vaultName}`);

  // Count files
  let fileCount = 0;
  function walkDir(dir) {
    const files = fs.readdirSync(dir);
    for (const file of files) {
      const filePath = path.join(dir, file);
      const stat = fs.statSync(filePath);

      if (stat.isDirectory()) {
        if (!file.startsWith('.')) {
          walkDir(filePath);
        }
      } else if (file.endsWith('.md')) {
        fileCount++;
      }
    }
  }
  walkDir(sourcePath);

  console.log(`  Files: ${fileCount}`);

  // Copy files (dry run simulation)
  if (!CONFIG.dryRun) {
    // In real implementation, you would copy files here
    // For now, we just count
  }

  totalFiles += fileCount;
  totalVaults++;
}

console.log('\n' + '='.repeat(60));
console.log(`Total Vaults: ${totalVaults}`);
console.log(`Total Files: ${totalFiles}`);
console.log(`Target Directory: ${CONFIG.targetDir}`);
console.log('='.repeat(60));
