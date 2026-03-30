import { Page, Locator, expect } from '@playwright/test';

/**
 * VoicePix Page Object Model
 *
 * Key UI element selectors (avoiding CSS class selectors per requirements):
 * - getByRole() / getByLabel() / getByText() primary
 * - data-testid noted where frontend cooperation would help
 */
export class VoicePixPage {
  readonly page: Page;
  readonly baseURL = 'http://localhost:8765';

  // ── Header ──────────────────────────────────────────────────────────────
  readonly langZhBtn: Locator;
  readonly langEnBtn: Locator;
  readonly apikeyBtn: Locator;

  // ── Navigation ─────────────────────────────────────────────────────────
  readonly tabT2A: Locator;
  readonly tabClone: Locator;

  // ── T2A Section ─────────────────────────────────────────────────────────
  readonly textInput: Locator;          // textarea#tText
  readonly voicePreset: Locator;        // select#preset
  readonly voiceGrid: Locator;           // #vgrid
  readonly speedSlider: Locator;        // input#spd
  readonly pitchSlider: Locator;        // input#pit
  readonly formatPills: Locator;        // .fpill buttons
  readonly generateBtn: Locator;         // #genBtn
  readonly outputBox: Locator;          // #outbox
  readonly playBtn: Locator;             // #playB (audio player)
  readonly downloadBtn: Locator;         // #dlBtn

  // ── Clone Section ────────────────────────────────────────────────────────
  readonly uploadZone: Locator;         // #uzone
  readonly fileInput: Locator;          // #fin (hidden)
  readonly cloneVoiceIdInput: Locator;  // #cvid
  readonly cloneBtn: Locator;            // #cloneBtn
  readonly cloneResult: Locator;         // #cloneRes

  // ── Modal ───────────────────────────────────────────────────────────────
  readonly modal: Locator;               // #modal
  readonly gidInput: Locator;            // #gidInput
  readonly keyInput: Locator;            // #keyInput
  readonly saveKeyBtn: Locator;          // .msave
  readonly deleteKeyBtn: Locator;        // .mdel button
  readonly closeModalBtn: Locator;        // .mclose

  // ── Toast ───────────────────────────────────────────────────────────────
  readonly toast: Locator;               // #toast

  // ── Status ───────────────────────────────────────────────────────────────
  readonly charCount: Locator;           // #cc

  constructor(page: Page) {
    this.page = page;

    // Header
    this.langZhBtn = page.getByRole('button', { name: '中文' });
    this.langEnBtn = page.getByRole('button', { name: /^EN$/ } );
    this.apikeyBtn = page.getByRole('button', { name: 'API Key' });

    // Navigation
    this.tabT2A = page.getByRole('button', { name: /文字转语音|Text to Speech/i });
    this.tabClone = page.getByRole('button', { name: /声音克隆|Voice Clone/i });

    // T2A
    this.textInput = page.locator('textarea[id="tText"]');
    this.voicePreset = page.locator('select[id="preset"]');
    this.voiceGrid = page.locator('#vgrid');
    this.speedSlider = page.locator('input[id="spd"]');
    this.pitchSlider = page.locator('input[id="pit"]');
    this.formatPills = page.locator('.fpill');
    this.generateBtn = page.locator('#genBtn');
    this.outputBox = page.locator('#outbox');
    this.playBtn = page.locator('#playB');
    this.downloadBtn = page.locator('#dlBtn');
    this.charCount = page.locator('#cc');

    // Clone
    this.uploadZone = page.locator('#uzone');
    this.fileInput = page.locator('input[type="file"][id="fin"]');
    this.cloneVoiceIdInput = page.locator('#cvid');
    this.cloneBtn = page.locator('#cloneBtn');
    this.cloneResult = page.locator('#cloneRes');

    // Modal
    this.modal = page.locator('#modal');
    this.gidInput = page.locator('#gidInput');
    this.keyInput = page.locator('#keyInput');
    this.saveKeyBtn = page.locator('.msave');
    this.deleteKeyBtn = page.locator('.mdel button');
    this.closeModalBtn = page.locator('.mclose');

    // Toast
    this.toast = page.locator('#toast');
  }

  async goto() {
    await this.page.goto(this.baseURL);
    // Wait for app to be fully rendered
    await this.page.waitForLoadState('networkidle');
    await this.tabT2A.waitFor({ state: 'visible' });
  }

  // ── Helpers ──────────────────────────────────────────────────────────────

  /** Open the API Key modal */
  async openApiKeyModal() {
    await this.apikeyBtn.click();
    await this.modal.waitFor({ state: 'visible' });
  }

  /** Close the API Key modal */
  async closeApiKeyModal() {
    await this.closeModalBtn.click();
    await this.modal.waitFor({ state: 'hidden' });
  }

  /** Set API Key via modal */
  async setApiKey(gid: string, key: string) {
    await this.openApiKeyModal();
    await this.gidInput.fill(gid);
    await this.keyInput.fill(key);
    await this.saveKeyBtn.click();
    await this.modal.waitFor({ state: 'hidden' });
    // Wait for button state update
    await this.page.waitForTimeout(200);
  }

  /** Delete API Key via modal */
  async deleteApiKey() {
    await this.openApiKeyModal();
    await this.deleteKeyBtn.click();
    await this.modal.waitFor({ state: 'hidden' });
  }

  /** Switch language */
  async switchLang(lang: 'zh' | 'en') {
    if (lang === 'en') {
      await this.langEnBtn.click();
    } else {
      await this.langZhBtn.click();
    }
    await this.page.waitForTimeout(100);
  }

  /** Click a voice item in the grid by its voice name text */
  async selectVoiceByName(name: string) {
    await this.page.getByText(name, { exact: true }).first().click();
  }

  /** Click voice preview button for a specific voice */
  async previewVoice(voiceName: string) {
    // The preview button is the ▶ button inside the vitem for the given voice
    const voiceItem = this.page.getByText(voiceName, { exact: true }).locator('..').locator('.vplay');
    await voiceItem.click();
  }

  /** Click a format pill */
  async selectFormat(format: 'mp3' | 'pcm' | 'wav' | 'flac') {
    await this.page.getByRole('button', { name: format.toUpperCase() }).click();
  }

  /** Upload a file to the clone upload zone */
  async uploadFile(filePath: string) {
    await this.fileInput.setInputFiles(filePath);
  }

  /** Get toast text (must be visible) */
  async getToastText(): Promise<string> {
    await this.toast.waitFor({ state: 'visible' });
    return this.toast.textContent() ?? '';
  }

  /** Check if output box (audio result) is visible */
  async isOutputVisible(): Promise<boolean> {
    return this.outputBox.isVisible();
  }

  /** Wait for toast to appear and return its text */
  async waitForToast(contains?: string): Promise<string> {
    await this.toast.waitFor({ state: 'visible' });
    if (contains) {
      await expect(this.toast).toContainText(contains);
    }
    return this.toast.textContent() ?? '';
  }

  /** Type text into the textarea */
  async typeText(text: string) {
    await this.textInput.fill(text);
  }

  /** Clear the textarea */
  async clearText() {
    await this.textInput.fill('');
  }
}
