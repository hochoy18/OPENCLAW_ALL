# MiniMax Studio - Speech & Image Visualization Platform

## Concept & Vision

A sleek, professional-grade web interface for exploring MiniMax's international API capabilities in Speech Synthesis and Image Generation. The design feels like a premium creative tool — think Vercel's dashboard meets Runway ML's creative energy. Dark mode with vibrant accent gradients that shift between warm coral (#FF6B6B) and electric violet (#7C3AED), conveying both creative power and technical precision.

---

## Design Language

### Aesthetic Direction
Premium dark creative tool — deep charcoal backgrounds with glass-morphism cards, gradient accents that pulse subtly, and smooth micro-interactions that make every action feel responsive and satisfying.

### Color Palette
```
--bg-primary: #0F0F12
--bg-secondary: #18181C
--bg-card: rgba(30, 30, 36, 0.8)
--bg-glass: rgba(255, 255, 255, 0.03)
--border-subtle: rgba(255, 255, 255, 0.08)
--border-glow: rgba(124, 58, 237, 0.3)

--text-primary: #FAFAFA
--text-secondary: #A1A1AA
--text-muted: #52525B

--accent-primary: #7C3AED (violet)
--accent-secondary: #EC4899 (pink)
--accent-gradient: linear-gradient(135deg, #7C3AED, #EC4899, #F97316)
--accent-glow: rgba(124, 58, 237, 0.4)

--success: #10B981
--warning: #F59E0B
--error: #EF4444

--speech-accent: #06B6D4 (cyan)
--image-accent: #F472B6 (pink)
```

### Typography
- **Headings**: Space Grotesk (700) — geometric, techy, distinctive
- **Body**: DM Sans (400, 500) — clean, highly readable
- **Monospace/Code**: JetBrains Mono — for API responses, JSON, voice IDs

### Spatial System
- Base unit: 4px
- Card padding: 24px
- Section gap: 48px
- Border radius: 12px (cards), 8px (buttons/inputs), 16px (large containers)

### Motion Philosophy
- **Page load**: Staggered fade-up (opacity 0→1, translateY 20px→0), 400ms ease-out, 80ms stagger
- **Card hover**: scale(1.02), box-shadow glow, 200ms ease
- **Button interactions**: scale(0.98) on press, gradient shift on hover
- **Tab transitions**: Sliding underline with gradient, 300ms cubic-bezier(0.4, 0, 0.2, 1)
- **Audio waveform**: Continuous subtle animation when playing
- **Loading states**: Gradient shimmer animation (left-to-right sweep)

### Visual Assets
- **Icons**: Lucide React (24px, stroke-width 1.5)
- **Decorative**: Gradient orbs in background (blurred, positioned absolutely), subtle grid pattern overlay
- **Voice visualization**: Custom SVG waveform animations
- **Image gallery**: Masonry-style grid with hover zoom

---

## Layout & Structure

### Overall Architecture
```
┌─────────────────────────────────────────────────────────────┐
│  Header: Logo + Tab Navigation (Speech | Image) + Theme    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Hero Section (contextual per tab)                   │   │
│  │  - Speech: "Transform Text into Natural Speech"     │   │
│  │  - Image: "Create Visual Masterpieces"              │   │
│  │  - Animated gradient text + feature badges          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌──────────────────┐  ┌────────────────────────────────┐   │
│  │                  │  │                                 │   │
│  │  Control Panel   │  │   Output / Preview Panel       │   │
│  │  (varies by tab) │  │   (varies by tab)               │   │
│  │                  │  │                                 │   │
│  │                  │  │                                 │   │
│  └──────────────────┘  └────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Feature Showcase / Capability Grid                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Voice/Model Catalog (scrollable, categorized)       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  Footer: API Status + Documentation Links                   │
└─────────────────────────────────────────────────────────────┘
```

### Responsive Strategy
- Desktop (>1200px): Two-column layout (controls 40% | preview 60%)
- Tablet (768-1200px): Stacked layout, full-width sections
- Mobile (<768px): Single column, collapsible sections

---

## Features & Interactions

### Speech (TTS) Tab

#### 1. Text Input Area
- Large textarea with live character count (max 10,000)
- Character counter changes color as approaching limit
- Placeholder with sample text
- **Actions**: Clear button (appears when text exists), paste from clipboard

#### 2. Voice Selection Panel
- **Voice Browser**: Categorized grid (Language → Type → Voice)
  - Categories: Chinese, English, Japanese, Korean, Spanish, etc.
  - Types: Male, Female, Character Voices
  - Each voice card shows: name, language tag, waveform preview icon
- **Search**: Filter voices by name or characteristic
- **Favorites**: Star voices to save for quick access
- **Voice Preview**: Play button on each voice card (sends "Hello, I'm [voice name]" to TTS)
- **Selected Voice**: Highlighted with gradient border, shows voice_id below

#### 3. Voice Parameters (Real-time Sliders)
| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| Speed | 0.5x - 2.0x | 1.0x | Playback speed |
| Pitch | -12 to +12 | 0 | Voice pitch adjustment |
| Volume | 0.1 - 10.0 | 1.0 | Output volume |
| Pause | 0.01s - 99.99s | (none) | Insert pause markers |

#### 4. Emotion Selector
- Grid of emotion chips: 😊 Happy, 😢 Sad, 😠 Angry, 😨 Fearful, 🤢 Disgusted, 😮 Surprised, 😐 Neutral
- Selected emotion glows with accent color
- Each emotion chip shows a small waveform icon

#### 5. Audio Settings
- **Format**: MP3 / WAV / PCM / FLAC (pill toggles)
- **Sample Rate**: 8000 / 16000 / 22050 / 24000 / 32000 / 44100 Hz
- **Bitrate**: 32000 / 64000 / 128000 / 256000 bps
- **Channel**: Mono / Stereo toggle

#### 6. Advanced Features
- **Pronunciation Overrides**: Add custom pronunciation for specific words/emojis
- **Timbre Mixing**: Blend two voices with adjustable weights (sliders)
- **Voice Effects**: Dropdown + preview — Spacious Echo, Studio Reverb, Phone Call, Radio, etc.
- **Language Boost**: Dropdown to enhance specific language recognition

#### 7. Generate Button
- Large gradient button with icon
- Loading state: animated gradient shimmer + "Generating..." text
- Disabled state when no text/voice selected

#### 8. Audio Output Panel
- **Waveform Visualization**: Animated SVG waveform when audio is playing
- **Playback Controls**: Play/Pause, Progress bar (draggable), Time display
- **Download Button**: Downloads the generated audio file
- **Share Button**: Copy shareable URL (if hosted)
- **Audio Info**: Duration, format, file size, voice used

#### 9. History Sidebar (Collapsible)
- List of recent generations with:
  - Text preview (truncated)
  - Voice used (icon + name)
  - Timestamp
  - Play / Re-generate buttons
- Click to reload settings

#### 10. Voice Clone/Design (Advanced Section)
- **Clone from Audio**: Upload audio file → Extract voice characteristics
- **Design Voice**: Text description → AI generates voice profile
- Status indicator for cloning/design process

---

### Image Tab

#### 1. Prompt Input
- Large textarea with AI-powered prompt enhancement suggestion
- **Prompt Templates**: Buttons for popular styles (Portrait, Landscape, Anime, Abstract, Product)
- Character/word counter
- **Negative Prompt**: Expandable section for things to exclude

#### 2. Reference Image (Img2Img)
- Drag-and-drop zone or click to upload
- Up to 5 reference images
- **Reference Modes**:
  - Style Transfer (preserve content, apply style)
  - Composition (use subject from ref, place in new scene)
  - Character Consistency (maintain identity across scenes)
  - Pan/Zoom (extend the image)
- Visual thumbnails of uploaded references with remove button

#### 3. Style Presets
- Grid of style cards with preview thumbnails:
  - Photorealistic, Anime, Digital Art, Oil Painting, Watercolor
  - Cyberpunk, Fantasy, Studio Portrait, Cinematic, Minimalist
- Each card shows a mini-preview image
- Multiple styles can be selected (for blending)

#### 4. Aspect Ratio & Resolution
- **Aspect Ratio**: 1:1, 3:4, 4:3, 9:16, 16:9, 2:1 (visual buttons)
- **Resolution**: 512x512, 768x768, 1024x1024, 1536x1536 (dropdown)

#### 5. Generation Parameters
| Parameter | Range | Default |
|-----------|-------|---------|
| Images Count | 1-4 | 1 |
| Seed | Random / Fixed | Random |
| Guidance Scale | 1-20 | 7.5 |
| Steps | 20-50 | 30 |

#### 6. Advanced Controls
- **Seed Control**: Number input + randomize button + seed history
- **Prompt Strength**: Slider for how much to follow prompt vs. creative freedom
- **Batch Generation**: Toggle to generate multiple variations

#### 7. Generate Button
- Gradient button with sparkle icon
- Progress indicator showing step count during generation

#### 8. Image Output Panel
- **Gallery View**: 
  - Masonry grid of generated images
  - Each image shows: hover overlay with actions (Download, Expand, Copy, Variations)
  - Click to expand to lightbox
- **Lightbox View**:
  - Full-screen image display
  - Zoom in/out controls
  - Download in original resolution
  - Show generation parameters used
  - Next/Previous navigation if multiple images

#### 9. Image Variations
- "Create Variations" button generates alternative versions
- Side-by-side comparison view (slider to compare original vs variation)

#### 10. History Sidebar
- Thumbnails of all generated images
- Click to reload prompt/parameters
- Delete/clear options

---

## Component Inventory

### Tab Navigation
- **Default**: Muted text, no background
- **Hover**: Text brightens, subtle underline appears
- **Active**: Gradient text (violet to pink), sliding underline with gradient
- **Transition**: 300ms with easing

### Voice/Feature Cards
- **Default**: Dark glass background, subtle border
- **Hover**: Elevated with glow shadow, slight scale
- **Selected**: Gradient border, inner glow
- **Disabled**: 50% opacity, no interactions

### Sliders
- **Track**: Dark with subtle gradient fill up to thumb
- **Thumb**: Gradient circle with glow on hover
- **Value Label**: Appears above thumb on drag
- **Real-time Preview**: Audio parameter changes preview in real-time

### Input Fields
- **Default**: Dark background, subtle border
- **Focus**: Gradient border glow, label floats up
- **Error**: Red border, error message below
- **Character Counter**: Bottom right, changes color at 80%/100%

### Buttons
- **Primary (Gradient)**: Violet-to-pink gradient, white text
  - Hover: Gradient shifts, glow intensifies
  - Active: scale(0.98)
  - Loading: Shimmer animation across surface
  - Disabled: Desaturated, no glow
- **Secondary**: Outlined with gradient border
- **Ghost**: Text only, subtle hover background

### Toggle Pills
- **Off**: Dark background, muted text
- **On**: Gradient background, white text
- **Transition**: Slide thumb with easing

### Waveform Visualization
- SVG path animated with CSS/JS
- Gradient fill (cyan for speech)
- Responds to audio playback in real-time

### Modal/Lightbox
- Backdrop: blur(12px) + dark overlay
- Content: Slide up + fade in
- Close button: Top right, hover glow

### Toast Notifications
- Bottom right, stacked
- Success (green), Error (red), Info (blue)
- Auto-dismiss with progress bar
- Hover pauses dismissal timer

---

## Technical Approach

### Frontend
- **Framework**: Single HTML file with vanilla JS (for portability)
- **Styling**: CSS custom properties, CSS Grid/Flexbox
- **Icons**: Lucide icons via CDN
- **Fonts**: Google Fonts (Space Grotesk, DM Sans, JetBrains Mono)
- **Audio**: Web Audio API for waveform visualization
- **Image Grid**: CSS Grid with masonry-like layout

### External Dependencies (CDN)
```html
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=DM+Sans:wght@400;500;600&family=JetBrains+Mono&display=swap">
<script src="https://unpkg.com/lucide@latest"></script>
```

### API Integration Points
For future backend integration:
- Speech TTS: MiniMax Speech 2.8 API (`POST /v1/t2a_v2`)
- Voice Catalog: MiniMax Voice List API (`POST /v1/get_voice`)
- Image Gen: MiniMax Image API
- WaveSpeed AI (alternative TTS endpoint)

### State Management
- Local state object for all form inputs
- LocalStorage for saving favorites, history, recent settings
- URL hash for sharing specific configurations

### Responsive Breakpoints
```css
/* Mobile first */
@media (min-width: 768px) { /* Tablet */ }
@media (min-width: 1200px) { /* Desktop */ }
```

---

## Page States

### Loading State
- Full-page skeleton with shimmer animation
- Gradient orbs pulse in background

### Empty State (No Output Yet)
- Centered illustration/icon
- Helpful prompt text: "Enter your text and select a voice to generate speech"

### Error State
- Red-tinted card with error icon
- Clear error message
- Retry button

### Success State
- Brief green flash/pulse
- Smooth transition to output view

---

## Micro-interactions

1. **Tab Switch**: Content slides out left, new content slides in right
2. **Voice Card Hover**: Plays a subtle "tick" sound preview (optional)
3. **Slider Drag**: Parameter value tooltip follows thumb
4. **Generate Click**: Button ripple effect + progress animation
5. **Audio Waveform**: Pulses with actual audio data
6. **Image Upload**: File icon animates into preview thumbnail
7. **Card Selection**: Gradient border animates clockwise
8. **Copy to Clipboard**: Brief "Copied!" tooltip
9. **Download**: File icon bounces briefly

---

## Accessibility

- All interactive elements keyboard accessible
- Focus states clearly visible (gradient ring)
- ARIA labels for icons and controls
- Reduced motion media query respected
- Color contrast meets WCAG AA
