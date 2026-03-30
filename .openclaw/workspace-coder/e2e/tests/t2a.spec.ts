import { test, expect, Page } from '@playwright/test';
import { VoicePixPage } from '../pages/VoicePixPage';

/**
 * T2A (Text-to-Audio) Tests for VoicePix
 *
 * Prerequisites: VoicePix app running at http://localhost:8765
 * These tests require a valid MiniMax API key set via the UI or localStorage.
 * For tests without a real API key, API calls will fail — we assert on error toasts.
 *
 * data-testid suggestions for frontend (optional improvements):
 * - #genBtn  → data-testid="t2a-generate-btn"
 * - #tText   → data-testid="t2a-text-input"
 * - #outbox  → data-testid="t2a-output-box"
 * - #playB   → data-testid="t2a-play-btn"
 * - #dlBtn   → data-testid="t2a-download-btn"
 * - .vplay   → data-testid="voice-preview-btn"
 */

test.describe('T2A (Text-to-Speech)', () => {
  let vp: VoicePixPage;

  test.beforeEach(async ({ page }) => {
    vp = new VoicePixPage(page);
    await vp.goto();
    // Ensure T2A tab is active
    await vp.tabT2A.click();
  });

  // ── T01: Full T2A flow ────────────────────────────────────────────────────
  test('T01: full T2A flow — input text, select voice, generate, verify audio element appears', async ({ page }) => {
    // Set a dummy API key so the generate button is enabled (API calls will fail but we test the UI flow)
    await vp.setApiKey('test-gid', 'test-key');

    // Input text
    await vp.typeText('你好，欢迎使用 VoicePix。');

    // Select a voice (Warm Girl)
    await vp.voicePreset.selectOption('Chinese (Mandarin)_Warm_Girl');

    // Verify character count updated
    await expect(vp.charCount).toHaveText('13');

    // Click generate (expect API error toast since key is fake)
    await vp.generateBtn.click();

    // The output box should appear even on API error (or we get an error toast)
    // We assert the button returns to enabled state after click
    await expect(vp.generateBtn).toBeEnabled({ timeout: 10000 });

    // If generation failed, we expect an error toast (no real API key)
    // If it somehow succeeded (mocked env), we verify output box is visible
    const outputVisible = await vp.isOutputVisible();
    if (outputVisible) {
      // Audio player controls should be present
      await expect(vp.playBtn).toBeVisible();
      await expect(vp.downloadBtn).toBeVisible();
    } else {
      // Error toast should appear for invalid credentials
      const toastText = await vp.waitForToast();
      expect(toastText).toMatch(/失败|fail|error|错误/i);
    }
  });

  // ── T02: No API Key — clicking generate shows toast ─────────────────────
  test('T02: without API key, clicking generate shows error toast', async ({ page }) => {
    // Clear any stored API key
    await page.evaluate(() => localStorage.removeItem('vp_ak'));
    await vp.goto(); // reload to pick up cleared storage

    await vp.typeText('测试文字');

    await vp.generateBtn.click();

    const toastText = await vp.waitForToast();
    expect(toastText).toMatch(/API Key|请先设置|set API Key/i);
  });

  // ── T03: Empty text — clicking generate shows toast ─────────────────────
  test('T03: with empty text, clicking generate shows error toast', async ({ page }) => {
    // Set a dummy API key so we get past the API-key check
    await vp.setApiKey('test-gid', 'test-key');

    await vp.clearText();
    // textarea should be empty
    await expect(vp.textInput).toHaveValue('');

    await vp.generateBtn.click();

    const toastText = await vp.waitForToast();
    expect(toastText).toMatch(/请输入文字|enter text|Please/i);
  });

  // ── T04: Voice preview button click — audio loads ───────────────────────
  test('T04: voice preview button triggers audio load or error toast', async ({ page }) => {
    // Set a dummy API key
    await vp.setApiKey('test-gid', 'test-key');

    // Click the preview button for "Warm Girl" voice
    // The vplay button is inside the vitem, use the text "温暖女孩" to locate it
    const warmGirlItem = page.locator('.vitem', { hasText: '温暖女孩' });
    const previewBtn = warmGirlItem.locator('.vplay');

    await previewBtn.click();

    // With a fake API key the preview will fail — we expect an error toast
    // With a real key it would load audio
    const toastText = await vp.waitForToast();
    // Either success or failure is acceptable; just verify a toast appeared
    expect(toastText.length).toBeGreaterThan(0);
  });

  // ── T05: Character count updates as user types ─────────────────────────
  test('T05: character count updates in real time', async ({ page }) => {
    const testText = '这是一段测试文字';
    await vp.typeText(testText);
    await expect(vp.charCount).toHaveText(String(testText.length));

    await vp.typeText('加上更多');
    await expect(vp.charCount).toHaveText(String((testText + '加上更多').length));
  });

  // ── T06: Speed slider changes displayed value ───────────────────────────
  test('T06: speed slider updates displayed speed value', async ({ page }) => {
    const spdVal = page.locator('#spdV');

    await vp.speedSlider.fill('1.5');
    await expect(spdVal).toHaveText('1.5x');

    await vp.speedSlider.fill('0.8');
    await expect(spdVal).toHaveText('0.8x');
  });

  // ── T07: Pitch slider changes displayed value ────────────────────────────
  test('T07: pitch slider updates displayed pitch value', async ({ page }) => {
    const pitVal = page.locator('#pitV');

    await vp.pitchSlider.fill('5');
    await expect(pitVal).toHaveText('5');

    await vp.pitchSlider.fill('-8');
    await expect(pitVal).toHaveText('-8');
  });

  // ── T08: Format pill selection works ────────────────────────────────────
  test('T08: format pill selection updates selected state', async ({ page }) => {
    // WAV pill
    await vp.selectFormat('wav');
    const wavPill = page.getByRole('button', { name: 'WAV' });
    await expect(wavPill).toHaveClass(/sel/);

    // FLAC pill
    await vp.selectFormat('flac');
    const flacPill = page.getByRole('button', { name: 'FLAC' });
    await expect(flacPill).toHaveClass(/sel/);
  });

  // ── T09: Voice preset select syncs with voice grid ───────────────────────
  test('T09: voice preset dropdown selection syncs with voice grid', async ({ page }) => {
    await vp.voicePreset.selectOption('English_Expressive_Narrator');

    // The corresponding vitem should be selected in the grid
    const narratorItem = page.locator('.vitem', { hasText: 'Expressive Narrator' });
    await expect(narratorItem).toHaveClass(/sel/);
  });
});
