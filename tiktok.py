#!/usr/bin/env python3
"""
AVENTAR TIKTOK VIDEO DOWNLOADER
=====================================
Single-file Python web server · Flask
No ads · No watermark · HD/4K · Video Preview Card

Requirements:
    pip install flask requests beautifulsoup4

Run:
    python tiktok.py
    Open:  http://localhost:5000
"""

from flask import Flask, request, jsonify, Response, render_template_string
import requests, re, urllib.parse, time, random, string

app = Flask(__name__)

# ─────────────────────────────────────────────────────────────
#  API CONFIG
# ─────────────────────────────────────────────────────────────
SSSTIK_API_URL = "https://ssstik.io/abc?url=dl"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Mobile Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-BD,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://ssstik.io",
    "Referer": "https://ssstik.io/",
    "hx-request": "true",
    "hx-trigger": "_gcaptcha_pt",
    "hx-target": "target",
    "hx-current-url": "https://ssstik.io/",
}

# ─────────────────────────────────────────────────────────────
#  HTML PAGE
# ─────────────────────────────────────────────────────────────
HTML_PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AVENTAR | TikTok Video Downloader</title>
<meta name="description" content="AVENTAR TikTok Video Downloader – Download TikTok videos HD/4K, no watermark, no ads.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&family=Noto+Sans+Bengali:wght@400;600&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#070710;--surface:#0f0f1a;--card:#161625;--card2:#1c1c2e;
  --border:#252540;--border2:#2e2e50;
  --accent:#7c3aed;--accent2:#a855f7;--accentg:linear-gradient(135deg,#7c3aed,#a855f7);
  --cyan:#06b6d4;--green:#10b981;--pink:#ec4899;--yellow:#f59e0b;
  --text:#e8eaf6;--muted:#8892b0;--muted2:#6272a4;
  --r:14px;
}
body{background:var(--bg);color:var(--text);font-family:'Space Grotesk',sans-serif;min-height:100vh;overflow-x:hidden}

/* BG GLOW */
.bg-glow{position:fixed;inset:0;pointer-events:none;z-index:0;overflow:hidden}
.bg-glow span{position:absolute;border-radius:50%;filter:blur(80px);opacity:.25}
.bg-glow span:nth-child(1){width:600px;height:600px;background:#7c3aed;top:-200px;left:-150px}
.bg-glow span:nth-child(2){width:500px;height:500px;background:#06b6d4;bottom:-180px;right:-120px}
.bg-glow span:nth-child(3){width:300px;height:300px;background:#ec4899;top:40%;left:50%;transform:translate(-50%,-50%)}

.wrap{position:relative;z-index:1;max-width:880px;margin:0 auto;padding:0 18px 70px}

/* ── HEADER ── */
header{text-align:center;padding:52px 20px 32px}
.brand-chip{
  display:inline-flex;align-items:center;gap:8px;
  background:rgba(124,58,237,.18);border:1px solid rgba(168,85,247,.35);
  color:#c4b5fd;border-radius:100px;padding:6px 16px 6px 10px;
  font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;margin-bottom:22px
}
.brand-chip svg{width:16px;height:16px;fill:currentColor}
h1{font-size:clamp(2rem,5.5vw,3.2rem);font-weight:800;line-height:1.08;margin-bottom:14px;
  background:linear-gradient(135deg,#fff 30%,#c084fc 70%,#67e8f9);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.tagline{color:var(--muted);font-size:.98rem;letter-spacing:.01em}
.pills{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin:22px 0 0}
.pill{
  display:inline-flex;align-items:center;gap:5px;
  background:rgba(124,58,237,.12);border:1px solid rgba(124,58,237,.25);
  color:#c4b5fd;border-radius:100px;padding:5px 13px;font-size:12.5px;font-weight:500
}

/* ── SEARCH BOX ── */
.search-card{
  background:var(--card);border:1px solid var(--border2);border-radius:var(--r);
  padding:26px 26px 22px;margin:28px 0 20px;
  box-shadow:0 0 0 1px rgba(124,58,237,.08),0 20px 60px rgba(0,0,0,.4)
}
.input-wrap{display:flex;gap:10px}
input[type=text]{
  flex:1;background:var(--surface);border:1.5px solid var(--border);border-radius:10px;
  color:var(--text);font-size:15px;padding:13px 16px;outline:none;
  transition:border-color .2s,box-shadow .2s;font-family:inherit
}
input[type=text]:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(124,58,237,.15)}
input[type=text]::placeholder{color:var(--muted2)}
.btn{
  padding:13px 22px;border:none;border-radius:10px;font-size:15px;font-weight:600;
  cursor:pointer;transition:opacity .18s,transform .1s;font-family:inherit;
  display:inline-flex;align-items:center;gap:7px;white-space:nowrap
}
.btn:active{transform:scale(.97)}
.btn-primary{background:var(--accentg);color:#fff}
.btn-primary:hover{opacity:.88}
.btn-primary:disabled{opacity:.45;cursor:not-allowed}

/* ── LOADER ── */
.loader{display:none;text-align:center;padding:36px;color:var(--muted);font-size:14px}
.spinner{
  width:38px;height:38px;border:3px solid var(--border2);border-top-color:var(--accent);
  border-radius:50%;animation:spin .65s linear infinite;margin:0 auto 14px
}
@keyframes spin{to{transform:rotate(360deg)}}

/* ── ERROR ── */
.error-box{
  display:none;background:rgba(239,68,68,.09);border:1px solid rgba(239,68,68,.28);
  color:#fca5a5;border-radius:10px;padding:13px 17px;font-size:14px;margin-top:14px
}

/* ══════════════════════════════════════════
   PREVIEW CARD  (the new big addition)
══════════════════════════════════════════ */
.preview-card{
  display:none;
  background:var(--card);border:1px solid var(--border2);border-radius:var(--r);
  overflow:hidden;margin-bottom:20px;
  box-shadow:0 0 0 1px rgba(124,58,237,.08),0 24px 70px rgba(0,0,0,.5);
  animation:fadeUp .35s ease
}
@keyframes fadeUp{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}

/* top: thumbnail + info side by side */
.preview-top{display:flex;gap:0}

/* LEFT thumbnail column */
.thumb-col{
  flex-shrink:0;width:180px;position:relative;background:#000;
  overflow:hidden
}
@media(max-width:560px){.thumb-col{width:120px}}
.thumb-col img{
  width:100%;height:100%;object-fit:cover;display:block;
  transition:transform .4s ease
}
.thumb-col:hover img{transform:scale(1.04)}
.thumb-overlay{
  position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
  background:rgba(0,0,0,.32);opacity:0;transition:opacity .25s
}
.thumb-col:hover .thumb-overlay{opacity:1}
.play-icon{
  width:48px;height:48px;background:rgba(124,58,237,.85);border-radius:50%;
  display:flex;align-items:center;justify-content:center;backdrop-filter:blur(4px)
}
.play-icon svg{width:20px;height:20px;fill:#fff;margin-left:3px}

/* quality ribbon */
.quality-ribbon{
  position:absolute;top:10px;left:0;
  background:linear-gradient(135deg,var(--accent),var(--accent2));
  color:#fff;font-size:10px;font-weight:700;letter-spacing:.06em;
  padding:3px 10px 3px 8px;border-radius:0 6px 6px 0;text-transform:uppercase
}

/* RIGHT info column */
.info-col{flex:1;padding:20px 22px;display:flex;flex-direction:column;gap:14px;min-width:0}

/* author row */
.author-row{display:flex;align-items:center;gap:12px}
.author-avatar{
  width:46px;height:46px;border-radius:50%;object-fit:cover;flex-shrink:0;
  border:2px solid var(--accent);box-shadow:0 0 0 3px rgba(124,58,237,.2)
}
.author-name{font-weight:700;font-size:15px;color:var(--text);line-height:1.2}
.author-handle{font-size:12px;color:var(--muted);margin-top:2px}

/* caption */
.video-caption{
  font-size:13.5px;color:var(--muted);line-height:1.55;
  display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden
}
.video-caption .hashtag{color:var(--cyan);font-weight:500}

/* stats row */
.stats-row{display:flex;flex-wrap:wrap;gap:10px}
.stat-chip{
  display:inline-flex;align-items:center;gap:6px;
  background:var(--surface);border:1px solid var(--border);
  border-radius:8px;padding:6px 12px;font-size:12.5px;color:var(--text);font-weight:500
}
.stat-chip svg{width:14px;height:14px;flex-shrink:0}
.stat-chip.likes svg{fill:#ec4899}.stat-chip.likes{color:#ec4899;border-color:rgba(236,72,153,.25);background:rgba(236,72,153,.07)}
.stat-chip.views svg{fill:#06b6d4}.stat-chip.views{color:#06b6d4;border-color:rgba(6,182,212,.25);background:rgba(6,182,212,.07)}
.stat-chip.comments svg{fill:#f59e0b}.stat-chip.comments{color:#f59e0b;border-color:rgba(245,158,11,.25);background:rgba(245,158,11,.07)}
.stat-chip.shares svg{fill:#10b981}.stat-chip.shares{color:#10b981;border-color:rgba(16,185,129,.25);background:rgba(16,185,129,.07)}
.stat-chip.duration svg{fill:#a855f7}.stat-chip.duration{color:#a855f7;border-color:rgba(168,85,247,.25);background:rgba(168,85,247,.07)}

/* music bar */
.music-bar{
  display:flex;align-items:center;gap:10px;
  background:var(--surface);border:1px solid var(--border);
  border-radius:9px;padding:9px 13px;font-size:13px;color:var(--muted);
  overflow:hidden
}
.music-icon{
  width:30px;height:30px;border-radius:50%;
  background:linear-gradient(135deg,var(--accent),var(--pink));
  display:flex;align-items:center;justify-content:center;flex-shrink:0
}
.music-icon svg{width:15px;height:15px;fill:#fff}
.music-text{flex:1;min-width:0}
.music-title{font-size:12.5px;font-weight:600;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.music-author{font-size:11.5px;color:var(--muted);margin-top:1px}
.music-disc{
  width:28px;height:28px;border-radius:50%;
  background:conic-gradient(#7c3aed,#ec4899,#06b6d4,#7c3aed);
  animation:discSpin 3s linear infinite;flex-shrink:0
}
@keyframes discSpin{to{transform:rotate(360deg)}}

/* ── DOWNLOAD SECTION (bottom of card) ── */
.download-section{
  background:var(--card2);border-top:1px solid var(--border);
  padding:18px 22px;display:flex;flex-direction:column;gap:10px
}
.dl-label{font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-bottom:2px}
.dl-btns{display:flex;gap:10px;flex-wrap:wrap}
.btn-dl{
  flex:1;min-width:160px;padding:13px 18px;border:none;border-radius:10px;
  font-size:14.5px;font-weight:700;cursor:pointer;font-family:inherit;
  display:inline-flex;align-items:center;justify-content:center;gap:8px;
  text-decoration:none;transition:opacity .18s,transform .1s
}
.btn-dl:active{transform:scale(.97)}
.btn-hd{background:linear-gradient(135deg,#059669,#10b981);color:#fff}
.btn-hd:hover{opacity:.88}
.btn-sd{background:rgba(16,185,129,.12);border:1px solid rgba(16,185,129,.3);color:#6ee7b7}
.btn-sd:hover{background:rgba(16,185,129,.2)}
.btn-mp3{background:linear-gradient(135deg,#0284c7,#06b6d4);color:#fff}
.btn-mp3:hover{opacity:.88}
.btn-mp3-wrap{display:none}

/* credit bar */
.credit-bar{
  display:flex;align-items:center;justify-content:space-between;
  font-size:11.5px;color:var(--muted2);padding-top:4px
}
.credit-bar strong{color:var(--accent2)}
.no-wm-tag{
  display:inline-flex;align-items:center;gap:4px;
  background:rgba(16,185,129,.12);border:1px solid rgba(16,185,129,.28);
  color:var(--green);border-radius:100px;padding:3px 10px;font-size:11px;font-weight:600
}

/* ── DESCRIPTION MODAL ── */
.desc-wrap{text-align:center;margin:24px 0 0}
.btn-desc{
  background:transparent;border:1.5px solid var(--border2);color:var(--muted);
  padding:10px 22px;border-radius:100px;font-size:13.5px;cursor:pointer;
  font-family:inherit;transition:all .2s
}
.btn-desc:hover{border-color:var(--accent);color:var(--text)}

.overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.75);backdrop-filter:blur(8px);z-index:200;align-items:center;justify-content:center;padding:18px}
.overlay.open{display:flex}
.modal{
  background:var(--card);border:1px solid var(--border2);border-radius:var(--r);
  max-width:640px;width:100%;max-height:90vh;overflow-y:auto;padding:32px;position:relative;
  animation:fadeUp .3s ease
}
.modal-close{position:absolute;top:14px;right:16px;background:var(--surface);border:1px solid var(--border);color:var(--muted);width:30px;height:30px;border-radius:50%;font-size:18px;cursor:pointer;display:flex;align-items:center;justify-content:center}
.modal h2{font-size:1.3rem;margin-bottom:5px}
.modal .sub{color:var(--muted);font-size:13px;margin-bottom:22px}
.dsec h3{color:var(--accent2);font-size:13px;text-transform:uppercase;letter-spacing:.07em;margin-bottom:8px;display:flex;align-items:center;gap:7px}
.dsec p{color:var(--muted);font-size:14px;line-height:1.72}
.dsec p.bn{font-family:'Noto Sans Bengali',sans-serif}
hr.d{border:none;border-top:1px solid var(--border);margin:18px 0}
.steps{list-style:none;counter-reset:s}
.steps li{counter-increment:s;display:flex;align-items:flex-start;gap:11px;margin-bottom:11px;font-size:14px;color:var(--muted);line-height:1.6}
.steps li::before{content:counter(s);min-width:22px;height:22px;background:var(--accentg);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#fff;flex-shrink:0;margin-top:2px}

/* ── FOOTER ── */
footer{text-align:center;padding:28px 20px;color:var(--muted2);font-size:13px;border-top:1px solid var(--border);margin-top:48px}
footer .brand{font-weight:800;color:var(--text);letter-spacing:.04em}
footer small{display:block;margin-top:5px;font-size:12px}

@media(max-width:500px){
  .input-wrap{flex-direction:column}
  .search-card{padding:18px}
  .info-col{padding:14px 16px}
  .dl-btns{flex-direction:column}
  .btn-dl{min-width:unset}
}
</style>
</head>
<body>
<div class="bg-glow"><span></span><span></span><span></span></div>
<div class="wrap">

<!-- ── HEADER ── -->
<header>
  <div class="brand-chip">
    <svg viewBox="0 0 24 24"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-2.88 2.5 2.89 2.89 0 0 1-2.89-2.89 2.89 2.89 0 0 1 2.89-2.89c.28 0 .54.04.79.1V9.01a6.33 6.33 0 0 0-.79-.05 6.34 6.34 0 0 0-6.34 6.34 6.34 6.34 0 0 0 6.34 6.34 6.34 6.34 0 0 0 6.33-6.34V8.69a8.24 8.24 0 0 0 4.81 1.54V6.78a4.85 4.85 0 0 1-1.04-.09z"/></svg>
    AVENTAR
  </div>
  <h1>TikTok Video<br>Downloader</h1>
  <p class="tagline">No Ads &nbsp;·&nbsp; No Watermark &nbsp;·&nbsp; HD / 4K &nbsp;·&nbsp; Instant</p>
  <div class="pills">
    <span class="pill">✓ Free Forever</span>
    <span class="pill">✓ No Watermark</span>
    <span class="pill">✓ 4K / HD</span>
    <span class="pill">✓ MP3 Audio</span>
    <span class="pill">✓ Zero Ads</span>
  </div>
</header>

<!-- ── SEARCH ── -->
<div class="search-card">
  <div class="input-wrap">
    <input type="text" id="urlInput" placeholder="Paste TikTok link here…  https://vm.tiktok.com/..." autocomplete="off" spellcheck="false"/>
    <button class="btn btn-primary" id="dlBtn" onclick="fetchVideo()">
      <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M12 16l-6-6h4V4h4v6h4l-6 6zm-8 4h16v-2H4v2z"/></svg>
      Download
    </button>
  </div>
  <div class="error-box" id="errBox"></div>
</div>

<!-- ── LOADER ── -->
<div class="loader" id="loader">
  <div class="spinner"></div>
  Fetching video info…
</div>

<!-- ══════════════════════════════════════════
     PREVIEW CARD
══════════════════════════════════════════ -->
<div class="preview-card" id="previewCard">

  <!-- TOP ROW: thumb + info -->
  <div class="preview-top">

    <!-- Thumbnail -->
    <div class="thumb-col">
      <img id="thumbImg" src="" alt="Video thumbnail">
      <div class="thumb-overlay">
        <div class="play-icon">
          <svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
        </div>
      </div>
      <div class="quality-ribbon" id="qualityRibbon">HD</div>
    </div>

    <!-- Info -->
    <div class="info-col">

      <!-- Author -->
      <div class="author-row">
        <img class="author-avatar" id="authorAvatar" src="" alt="Author">
        <div>
          <div class="author-name" id="authorName">—</div>
          <div class="author-handle" id="authorHandle"></div>
        </div>
      </div>

      <!-- Caption / Tags -->
      <div class="video-caption" id="videoCaption"></div>

      <!-- Stats -->
      <div class="stats-row" id="statsRow">
        <!-- filled by JS -->
      </div>

      <!-- Music -->
      <div class="music-bar" id="musicBar" style="display:none">
        <div class="music-icon">
          <svg viewBox="0 0 24 24"><path d="M12 3v10.55A4 4 0 1 0 14 17V7h4V3h-6z"/></svg>
        </div>
        <div class="music-text">
          <div class="music-title" id="musicTitle">Original Sound</div>
          <div class="music-author" id="musicAuthor"></div>
        </div>
        <div class="music-disc"></div>
      </div>

    </div><!-- /info-col -->
  </div><!-- /preview-top -->

  <!-- DOWNLOAD SECTION -->
  <div class="download-section">
    <div class="dl-label">Download Options</div>
    <div class="dl-btns">
      <a class="btn-dl btn-hd" id="btnHD" href="#" target="_blank" rel="noopener">
        <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M12 16l-6-6h4V4h4v6h4l-6 6zm-8 4h16v-2H4v2z"/></svg>
        Download HD · No Watermark
      </a>
      <a class="btn-dl btn-sd" id="btnSD" href="#" target="_blank" rel="noopener" style="display:none">
        <svg width="15" height="15" fill="currentColor" viewBox="0 0 24 24"><path d="M12 16l-6-6h4V4h4v6h4l-6 6zm-8 4h16v-2H4v2z"/></svg>
        SD Quality
      </a>
    </div>
    <div class="btn-mp3-wrap" id="mp3Wrap">
      <a class="btn-dl btn-mp3" id="btnMP3" href="#" target="_blank" rel="noopener">
        <svg width="15" height="15" fill="currentColor" viewBox="0 0 24 24"><path d="M12 3v10.55A4 4 0 1 0 14 17V7h4V3h-6z"/></svg>
        Download MP3 Audio
      </a>
    </div>
    <div class="credit-bar">
      <span>by <strong>AVENTAR</strong></span>
      <span class="no-wm-tag">✓ Watermark Free</span>
    </div>
  </div>

</div><!-- /preview-card -->

<!-- ── HOW IT WORKS button ── -->
<div class="desc-wrap">
  <button class="btn-desc" onclick="document.getElementById('descModal').classList.add('open')">
    📖 How It Works &nbsp;/&nbsp; কিভাবে কাজ করে
  </button>
</div>

</div><!-- /wrap -->

<!-- ══════════════════════════════════════════
     DESCRIPTION MODAL
══════════════════════════════════════════ -->
<div class="overlay" id="descModal" onclick="if(event.target===this)this.classList.remove('open')">
  <div class="modal">
    <button class="modal-close" onclick="document.getElementById('descModal').classList.remove('open')">×</button>
    <h2>AVENTAR TikTok Downloader</h2>
    <p class="sub">English + বাংলা গাইড</p>

    <div class="dsec">
      <h3>🇬🇧 What is this?</h3>
      <p>AVENTAR TikTok Video Downloader is a free, ad-free web tool to download TikTok videos in the highest available quality (HD / 4K) without any watermark. You can also extract the audio as an MP3. No login required, no annoying ads, completely free.</p>
    </div>
    <hr class="d">
    <div class="dsec">
      <h3>🇬🇧 How to use</h3>
      <ol class="steps">
        <li>Open TikTok and find the video you want to download.</li>
        <li>Tap <strong>Share → Copy Link</strong> to copy the video URL.</li>
        <li>Come back here, paste the link into the box at the top.</li>
        <li>Click <strong>Download</strong> — the video preview & info will appear instantly.</li>
        <li>Click <strong>Download HD · No Watermark</strong> to save the video in best quality, or <strong>Download MP3</strong> for audio only.</li>
      </ol>
    </div>
    <hr class="d">
    <div class="dsec">
      <h3>🇧🇩 এটি কী?</h3>
      <p class="bn">AVENTAR TikTok ভিডিও ডাউনলোডার একটি সম্পূর্ণ বিনামূল্যে ও বিজ্ঞাপনমুক্ত ওয়েব টুল। এখান থেকে আপনি TikTok-এর যেকোনো ভিডিও সর্বোচ্চ মানে (HD / 4K) ওয়াটারমার্ক ছাড়াই ডাউনলোড করতে পারবেন। MP3 অডিওও সরাসরি ডাউনলোড করা যাবে। কোনো অ্যাকাউন্ট বা লগইন লাগবে না।</p>
    </div>
    <hr class="d">
    <div class="dsec">
      <h3>🇧🇩 কিভাবে ব্যবহার করবেন</h3>
      <ol class="steps">
        <li>TikTok অ্যাপ খুলুন এবং পছন্দের ভিডিওটি খুঁজুন।</li>
        <li><strong>শেয়ার → লিঙ্ক কপি করুন</strong> (Copy Link) ট্যাপ করুন।</li>
        <li>এই ওয়েবসাইটে ফিরে উপরের বক্সে লিঙ্কটি পেস্ট করুন।</li>
        <li><strong>Download</strong> বাটনে ক্লিক করুন — ভিডিওর প্রিভিউ ও তথ্য দেখা যাবে।</li>
        <li><strong>Download HD · No Watermark</strong> ক্লিক করে ভিডিও সেভ করুন অথবা শুধু অডিও চাইলে <strong>Download MP3</strong> বেছে নিন।</li>
      </ol>
    </div>
    <hr class="d">
    <div class="dsec">
      <h3>⚙️ Technical Details</h3>
      <p>Your TikTok URL is sent server-side to the ssstik.io backend API with proper authentication headers (hx-request, hx-trigger, Referer). The response HTML is parsed to extract direct CDN links from tikcdn.io. A built-in proxy streams the file to your browser, bypassing watermarks, ads, and CORS restrictions entirely. No data is stored.</p>
    </div>
    <hr class="d">
    <div class="dsec">
      <h3>🔒 Privacy</h3>
      <p>কোনো ভিডিও বা ব্যক্তিগত তথ্য আমাদের সার্ভারে সংরক্ষণ করা হয় না। সব লিঙ্ক রিয়েল-টাইমে ফেচ করা হয়। / No video or personal data is stored on our servers. All links are fetched in real-time.</p>
    </div>
    <hr class="d">
    <div style="text-align:center;padding:8px 0;color:var(--muted2);font-size:13px">
      Made with ❤️ by <strong style="color:var(--accent2)">AVENTAR</strong> &nbsp;·&nbsp; All rights reserved &copy; 2025–2026
    </div>
  </div>
</div>

<!-- ── FOOTER ── -->
<footer>
  <span class="brand">AVENTAR</span> TikTok Video Downloader
  &nbsp;·&nbsp; No Ads · No Watermark · Full HD / 4K
  &nbsp;·&nbsp; &copy; 2025–2026
  <small>Not affiliated with TikTok, Douyin or ByteDance. &nbsp;|&nbsp; Made by AVENTAR</small>
</footer>

<script>
// ── paste/enter shortcut ──
const inp = document.getElementById('urlInput');
inp.addEventListener('paste', () => setTimeout(() => { if(inp.value.trim()) fetchVideo(); }, 80));
inp.addEventListener('keydown', e => { if(e.key==='Enter') fetchVideo(); });

function formatNum(n){
  if(!n && n!==0) return '—';
  n = parseInt(n);
  if(isNaN(n)) return n;
  if(n >= 1000000) return (n/1000000).toFixed(1).replace(/\.0$/,'')+'M';
  if(n >= 1000)    return (n/1000).toFixed(1).replace(/\.0$/,'')+'K';
  return n.toString();
}

function highlightHashtags(text){
  if(!text) return '';
  return text.replace(/(#\w+)/g, '<span class="hashtag">$1</span>');
}

async function fetchVideo(){
  const url = inp.value.trim();
  if(!url){ showErr('Please paste a TikTok URL first.'); return; }
  if(!url.includes('tiktok') && !url.includes('douyin')){
    showErr('Not a valid TikTok URL. Please copy the link from TikTok app.');
    return;
  }
  hideErr();
  setLoading(true);
  hidePreview();

  try{
    const r = await fetch('/api/download',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({url})
    });
    const d = await r.json();
    if(!r.ok || d.error){ showErr(d.error||'Failed to fetch. Try again.'); return; }
    renderPreview(d);
  } catch(e){
    showErr('Network error. Check your connection and try again.');
  } finally {
    setLoading(false);
  }
}

function renderPreview(d){
  // thumbnail
  document.getElementById('thumbImg').src = d.thumbnail || '';

  // quality ribbon
  const rib = document.getElementById('qualityRibbon');
  rib.textContent = d.hd_url ? 'HD · 4K' : 'SD';
  rib.style.background = d.hd_url
    ? 'linear-gradient(135deg,#7c3aed,#a855f7)'
    : 'linear-gradient(135deg,#0284c7,#06b6d4)';

  // author
  document.getElementById('authorAvatar').src = d.avatar || '';
  document.getElementById('authorName').textContent = d.author || 'TikTok User';
  document.getElementById('authorHandle').textContent = d.handle ? '@'+d.handle : '';

  // caption
  document.getElementById('videoCaption').innerHTML = highlightHashtags(d.description || '');

  // stats
  const statsRow = document.getElementById('statsRow');
  statsRow.innerHTML = '';
  const stats = [
    {key:'likes',    icon:'<svg viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>', label:'Likes',    val:d.likes},
    {key:'views',    icon:'<svg viewBox="0 0 24 24"><path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zm0 12.5a5 5 0 1 1 0-10 5 5 0 0 1 0 10zm0-8a3 3 0 1 0 0 6 3 3 0 0 0 0-6z"/></svg>', label:'Views',    val:d.views},
    {key:'comments', icon:'<svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>', label:'Comments', val:d.comments},
    {key:'shares',   icon:'<svg viewBox="0 0 24 24"><path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11A2.99 2.99 0 0 0 18 8a3 3 0 1 0-3-3c0 .24.04.47.09.7L8.04 9.81A2.99 2.99 0 0 0 6 9a3 3 0 0 0 0 6c.79 0 1.5-.31 2.04-.81l7.12 4.15c-.05.21-.08.43-.08.66a2.99 2.99 0 1 0 3-3z"/></svg>', label:'Shares',   val:d.shares},
    {key:'duration', icon:'<svg viewBox="0 0 24 24"><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zm4.24 14.24L11 13V7h1.5v5.25l4.5 2.67-1.76 1.32z"/></svg>', label:'Duration', val:d.duration},
  ];
  stats.forEach(s => {
    if(!s.val && s.val!==0) return;
    const c = document.createElement('span');
    c.className = 'stat-chip '+s.key;
    c.innerHTML = s.icon + formatNum(s.val) + ' ' + s.label;
    statsRow.appendChild(c);
  });

  // music
  if(d.music_title){
    document.getElementById('musicTitle').textContent  = d.music_title;
    document.getElementById('musicAuthor').textContent = d.music_author || '';
    document.getElementById('musicBar').style.display  = 'flex';
  } else {
    document.getElementById('musicBar').style.display = 'none';
  }

  // download buttons
  const btnHD = document.getElementById('btnHD');
  const btnSD = document.getElementById('btnSD');
  const mp3Wrap = document.getElementById('mp3Wrap');
  const btnMP3 = document.getElementById('btnMP3');

  if(d.hd_url){
    btnHD.href = '/api/proxy?url=' + encodeURIComponent(d.hd_url);
    btnHD.setAttribute('download','AVENTAR_tiktok_hd.mp4');
    btnHD.style.display = 'inline-flex';
  } else {
    btnHD.style.display = 'none';
  }

  if(d.sd_url){
    btnSD.href = '/api/proxy?url=' + encodeURIComponent(d.sd_url);
    btnSD.setAttribute('download','AVENTAR_tiktok_sd.mp4');
    btnSD.style.display = d.hd_url ? 'inline-flex' : 'inline-flex';
  } else {
    btnSD.style.display = 'none';
  }

  if(d.mp3_url){
    btnMP3.href = '/api/proxy?url=' + encodeURIComponent(d.mp3_url);
    btnMP3.setAttribute('download','AVENTAR_audio.mp3');
    mp3Wrap.style.display = 'block';
  } else {
    mp3Wrap.style.display = 'none';
  }

  document.getElementById('previewCard').style.display = 'block';
  document.getElementById('previewCard').scrollIntoView({behavior:'smooth', block:'nearest'});
}

function setLoading(v){
  document.getElementById('loader').style.display = v ? 'block' : 'none';
  document.getElementById('dlBtn').disabled = v;
}
function hidePreview(){ document.getElementById('previewCard').style.display='none'; }
function showErr(m){ const b=document.getElementById('errBox'); b.innerHTML='⚠ '+m; b.style.display='block'; }
function hideErr(){ document.getElementById('errBox').style.display='none'; }
</script>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────

def rnd_token(n=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


def parse_ssstik(html: str) -> dict:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    r = {}

    # ── author ──
    for cls in ['maintext', 'tiktok-name', 'author-name']:
        t = soup.find(class_=cls)
        if t: r['author'] = t.get_text(strip=True); break
    if 'author' not in r:
        t = soup.find('h2') or soup.find('h3')
        r['author'] = t.get_text(strip=True) if t else 'TikTok User'

    # ── handle ──
    for cls in ['maintext2', 'tiktok-handle', 'author-handle']:
        t = soup.find(class_=cls)
        if t: r['handle'] = t.get_text(strip=True).lstrip('@'); break

    # ── description/tags ──
    for cls in ['tag', 'desc', 'description', 'video-desc']:
        t = soup.find(class_=cls)
        if t: r['description'] = t.get_text(strip=True); break
    if 'description' not in r:
        t = soup.find('p')
        r['description'] = t.get_text(strip=True) if t else ''

    # ── avatar ──
    av = soup.find('img', class_='result_author')
    if not av:
        av = soup.find('img', class_=lambda c: c and 'avatar' in c.lower())
    r['avatar'] = av['src'] if av else ''

    # ── thumbnail ──
    th = soup.find('img', class_='result_video_cover')
    if not th:
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if ('tikcdn' in src or 'tiktokcdn' in src) and 'avatar' not in src:
                th = img; break
    r['thumbnail'] = th['src'] if th else (r.get('avatar',''))

    # ── stats: try data-* attributes and text patterns ──
    stats_map = {'likes': None, 'views': None, 'comments': None, 'shares': None, 'duration': None}
    # look for data attributes
    for tag in soup.find_all(True):
        for attr in tag.attrs:
            v = tag[attr]
            al = attr.lower()
            if 'like'    in al and stats_map['likes']    is None: stats_map['likes']    = v
            if 'view'    in al and stats_map['views']    is None: stats_map['views']    = v
            if 'comment' in al and stats_map['comments'] is None: stats_map['comments'] = v
            if 'share'   in al and stats_map['shares']   is None: stats_map['shares']   = v

    # text patterns like "1.2M likes"
    full_text = soup.get_text()
    for pattern, key in [
        (r'([\d,.]+[KMB]?)\s*likes?', 'likes'),
        (r'([\d,.]+[KMB]?)\s*views?', 'views'),
        (r'([\d,.]+[KMB]?)\s*comments?', 'comments'),
        (r'([\d,.]+[KMB]?)\s*shares?', 'shares'),
        (r'(\d+:\d+)', 'duration'),
    ]:
        m = re.search(pattern, full_text, re.I)
        if m and stats_map[key] is None:
            stats_map[key] = m.group(1)

    r.update({k: v for k, v in stats_map.items() if v})

    # ── music ──
    for cls in ['music-title', 'music_title', 'sound-name', 'music-info']:
        t = soup.find(class_=cls)
        if t: r['music_title'] = t.get_text(strip=True); break
    # fallback regex
    if 'music_title' not in r:
        m = re.search(r'original sound\s*[-–]\s*(.+)', full_text, re.I)
        if m: r['music_title'] = m.group(0)

    # ── download links ──
    hd_url = sd_url = mp3_url = ''
    for a in soup.find_all('a', href=True):
        href = a['href']
        if not href or href == '#': continue
        text = a.get_text(' ', strip=True).lower()
        cls  = ' '.join(a.get('class', [])).lower()

        is_cdn = 'tikcdn.io' in href or 'tiktokcdn' in href or 'tiktok.com/video' in href

        if 'mp3' in text or 'music' in text or 'audio' in text or 'mp3' in href.lower():
            if not mp3_url: mp3_url = href
        elif ('hd' in text or 'without' in text or 'no watermark' in text or
              'hd' in cls or 'nowatermark' in cls or 'no_watermark' in href.lower() or
              ('download' in text and not sd_url)):
            if not hd_url and is_cdn: hd_url = href
            elif not hd_url: hd_url = href
        elif is_cdn and not sd_url:
            sd_url = href

    # fallback: grab all tikcdn links in order
    if not hd_url:
        cdn_links = [a['href'] for a in soup.find_all('a', href=True)
                     if ('tikcdn.io' in a.get('href','') or 'tiktokcdn' in a.get('href',''))
                     and 'mp3' not in a.get('href','').lower()]
        if cdn_links: hd_url = cdn_links[0]
        if len(cdn_links) > 1: sd_url = cdn_links[1]

    r['hd_url']  = hd_url
    r['sd_url']  = sd_url
    r['mp3_url'] = mp3_url
    r['quality_label'] = 'HD / 4K · No Watermark' if hd_url else 'SD Quality'
    return r


# ─────────────────────────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)


@app.route('/api/download', methods=['POST'])
def api_download():
    body = request.get_json(force=True, silent=True) or {}
    tiktok_url = (body.get('url') or '').strip()
    if not tiktok_url:
        return jsonify({'error': 'No URL provided.'}), 400

    payload = urllib.parse.urlencode({
        'id': tiktok_url,
        'locale': 'en',
        'tt': rnd_token(),
    })

    try:
        resp = requests.post(SSSTIK_API_URL, headers=HEADERS, data=payload, timeout=22)
        resp.raise_for_status()
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timed out. Please try again.'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Upstream error: {e}'}), 502

    html = resp.text
    if not html or len(html) < 40:
        return jsonify({'error': 'Empty response. The link may be private or invalid.'}), 502

    try:
        data = parse_ssstik(html)
    except Exception as e:
        return jsonify({'error': f'Parse error: {e}'}), 500

    if not data.get('hd_url') and not data.get('sd_url'):
        return jsonify({'error': 'Could not extract download links. Video may be private or region-locked.'}), 404

    return jsonify(data)


@app.route('/api/proxy')
def api_proxy():
    cdn_url = request.args.get('url', '').strip()
    if not cdn_url:
        return 'Missing url', 400

    allowed = ('tikcdn.io', 'tiktokcdn', 'tiktok.com', 'muscdn.com', 'akamaized.net', 'sgpstatp')
    if not any(d in cdn_url for d in allowed):
        return 'Disallowed domain', 403

    proxy_h = {'User-Agent': HEADERS['User-Agent'], 'Referer': 'https://ssstik.io/', 'Accept': '*/*'}
    try:
        up = requests.get(cdn_url, headers=proxy_h, stream=True, timeout=90)
        up.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f'Proxy error: {e}', 502

    ctype = up.headers.get('Content-Type', 'application/octet-stream')

    def stream():
        for chunk in up.iter_content(chunk_size=65536):
            if chunk: yield chunk

    ext = 'mp3' if 'mp3' in cdn_url.lower() or 'audio' in ctype else 'mp4'
    fname = f'AVENTAR_TikTok_{int(time.time())}.{ext}'
    res = Response(stream(), content_type=ctype)
    res.headers['Content-Disposition'] = f'attachment; filename="{fname}"'
    res.headers['Content-Length']      = up.headers.get('Content-Length', '')
    res.headers['Accept-Ranges']       = 'bytes'
    return res


# ─────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("╔══════════════════════════════════════════════╗")
    print("║   AVENTAR TikTok Video Downloader       ║")
    print("║   http://localhost:5000                       ║")
    print("╚══════════════════════════════════════════════╝")
    app.run(host='0.0.0.0', port=11110, debug=False)
