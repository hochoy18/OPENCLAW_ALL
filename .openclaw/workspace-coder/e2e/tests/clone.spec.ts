import { test, expect } from '@playwright/test';
import { VoicePixPage } from '../pages/VoicePixPage';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Clone (Voice Clone) Tests for VoicePix
 *
 * Prerequisites: VoicePix app running at http://localhost:8765
 *
 * data-testid suggestions for frontend (optional improvements):
 * - #uzone  → data-testid="clone-upload-zone"
 * - #fin    → data-testid="clone-file-input"
 * - #cvid   → data-testid="clone-voice-id-input"
 * - #cloneBtn → data-testid="clone-submit-btn"
 * - #cloneRes → data-testid="clone-result-box"
 */

test.describe('Voice Clone', () => {
  let vp: VoicePixPage;

  // A minimal valid MP3 file (or use a real small audio fixture)
  const tmpAudioFile = path.join(__dirname, 'fixtures', 'test-voice.mp3');
  const tmpTextFile = path.join(__dirname, 'fixtures', 'test-text.txt');

  test.beforeAll(() => {
    // Create fixture directory and a minimal fake audio file for testing
    const fixtureDir = path.join(__dirname, 'fixtures');
    if (!fs.existsSync(fixtureDir)) {
      fs.mkdirSync(fixtureDir, { recursive: true });
    }
    // Write minimal MP3 header (not a real MP3, just enough to pass file-type checks in UI)
    // The UI checks extension (.mp3), not actual MIME type for the upload zone
    fs.writeFileSync(tmpAudioFile, Buffer.from([0xFF, 0xFB, 0x90, 0x00]));
    fs.writeFileSync(tmpTextFile, Buffer.from('This is a text file, not audio.'));
  });

  test.afterAll(() => {
    // Clean up fixtures
    try { fs.unlinkSync(tmpAudioFile); } catch {}
    try { fs.unlinkSync(tmpTextFile); } catch {}
  });

  test.beforeEach(async ({ page }) => {
    vp = new VoicePixPage(page);
    await vp.goto();
    // Switch to Clone tab
    await vp.tabClone.click();
    await vp.cloneBtn.waitFor({ state: 'visible' });
  });

  // ── T10: Upload non-audio file → error toast ─────────────────────────────
  test('T10: uploading a non-audio file shows error toast', async ({ page }) => {
    // Upload a text file (wrong extension)
    await vp.fileInput.setInputFiles(tmpTextFile);

    // The UI validates file by extension, so uploading .txt should still accept it in the input
    // but the toast for invalid type fires when the API call happens
    // We check that the filename is displayed in ufname
    const fname = page.locator('#fname');
    await expect(fname).toBeVisible();
    await expect(fname).toContainText('test-text.txt');

    // Click clone — should fail with error about file type
    await vp.setApiKey('test-gid', 'test-key');
    await vp.cloneVoiceIdInput.fill('test_voice_id_t10');
    await vp.cloneBtn.click();

    // The API call with a .txt file should fail at MiniMax side
    const toastText = await vp.waitForToast();
    expect(toastText.length).toBeGreaterThan(0);
  });

  // ── T11: Clone without uploading any file ───────────────────────────────
  test('T11: clicking clone without uploading a file shows error toast', async ({ page }) => {
    await vp.setApiKey('test-gid', 'test-key');

    // Don't upload any file
    await vp.cloneVoiceIdInput.fill('test_voice_id_t11');
    await vp.cloneBtn.click();

    const toastText = await vp.waitForToast();
    expect(toastText).toMatch(/上传|upload|audio/i);
  });

  // ── T12: Clone with empty voice_id → error toast ────────────────────────
  test('T12: clicking clone with empty voice_id shows error toast', async ({ page }) => {
    await vp.setApiKey('test-gid', 'test-key');

    // Upload a file but leave voice_id empty
    await vp.fileInput.setInputFiles(tmpAudioFile);
    await expect(page.locator('#fname')).toContainText('test-voice.mp3');

    await vp.cloneVoiceIdInput.fill('');
    await vp.cloneBtn.click();

    const toastText = await vp.waitForToast();
    expect(toastText).toMatch(/声音ID|voice ID|enter/i);
  });

  // ── T13: Uploaded file name is displayed ───────────────────────────────
  test('T13: uploaded file name is shown in upload zone', async ({ page }) => {
    await vp.fileInput.setInputFiles(tmpAudioFile);
    const fname = page.locator('#fname');
    await expect(fname).toBeVisible();
    await expect(fname).toContainText('test-voice.mp3');
  });

  // ── T14: Clone result area is hidden initially ───────────────────────────
  test('T14: clone result area is hidden before any clone attempt', async ({ page }) => {
    await expect(vp.cloneResult).toBeHidden();
  });

  // ── T15: Navigate to clone tab and back to T2A ─────────────────────────
  test('T15: can switch between Clone and T2A tabs', async ({ page }) => {
    // Already on Clone tab
    await expect(page.locator('#s-clone')).toHaveClass(/on/);
    await expect(page.locator('#s-t2a')).not.toHaveClass(/on/);

    // Switch to T2A
    await vp.tabT2A.click();
    await expect(page.locator('#s-t2a')).toHaveClass(/on/);
    await expect(page.locator('#s-clone')).not.toHaveClass(/on/);
  });
});
