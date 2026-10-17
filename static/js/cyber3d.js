/**
 * =====================================================================
 * ScamShield AI - Cyber3D Engine (Three.js & 3D Spatial Aesthetics)
 * Features:
 *   1. Global Interactive WebGL Cyber Background Field
 *   2. Hero Interactive 3D Holographic Shield & Gyro Defense Core
 *   3. Dashboard Interactive 3D Cyber Threat Globe
 *   4. Zero-Dependency 3D Perspective Card Tilt & Dynamic Glare
 *   5. Web Audio API Sci-Fi Cyber Sound Synthesizer
 * =====================================================================
 */

(function () {
  'use strict';

  // -------------------------------------------------------------
  // 1. Web Audio API Sci-Fi Synthesizer (Zero External Assets)
  // -------------------------------------------------------------
  const CyberAudio = {
    ctx: null,
    enabled: true,

    init() {
      const stored = localStorage.getItem('scamshield_sfx');
      this.enabled = stored !== null ? stored === 'true' : true;
      this.updateUI();
    },

    getContext() {
      if (!this.ctx && (window.AudioContext || window.webkitAudioContext)) {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        this.ctx = new AudioCtx();
      }
      if (this.ctx && this.ctx.state === 'suspended') {
        this.ctx.resume();
      }
      return this.ctx;
    },

    toggle() {
      this.enabled = !this.enabled;
      localStorage.setItem('scamshield_sfx', this.enabled ? 'true' : 'false');
      this.updateUI();
      if (this.enabled) {
        this.playBeep(880, 'sine', 0.08, 0.15);
      }
      return this.enabled;
    },

    updateUI() {
      const btn = document.getElementById('sfxToggleBtn');
      if (btn) {
        btn.innerHTML = this.enabled
          ? `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg> <span>SFX ON</span>`
          : `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><line x1="23" y1="9" x2="17" y2="15"></line><line x1="17" y1="9" x2="23" y2="15"></line></svg> <span>SFX OFF</span>`;
        btn.classList.toggle('active', this.enabled);
      }
    },

    playBeep(freq = 600, type = 'sine', duration = 0.05, gainVal = 0.08) {
      if (!this.enabled) return;
      try {
        const ctx = this.getContext();
        if (!ctx) return;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, ctx.currentTime);
        gain.gain.setValueAtTime(gainVal, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + duration);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + duration);
      } catch (e) {}
    },

    playScanLaser() {
      if (!this.enabled) return;
      try {
        const ctx = this.getContext();
        if (!ctx) return;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(1400, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(220, ctx.currentTime + 0.35);
        gain.gain.setValueAtTime(0.08, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.35);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.35);
      } catch (e) {}
    },

    playAlert(isDanger = false) {
      if (!this.enabled) return;
      try {
        const ctx = this.getContext();
        if (!ctx) return;
        const now = ctx.currentTime;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        if (isDanger) {
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(440, now);
          osc.frequency.setValueAtTime(330, now + 0.12);
          osc.frequency.setValueAtTime(220, now + 0.24);
          gain.gain.setValueAtTime(0.12, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.4);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start();
          osc.stop(now + 0.4);
        } else {
          osc.type = 'sine';
          osc.frequency.setValueAtTime(523.25, now);
          osc.frequency.setValueAtTime(659.25, now + 0.08);
          osc.frequency.setValueAtTime(783.99, now + 0.16);
          gain.gain.setValueAtTime(0.1, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start();
          osc.stop(now + 0.35);
        }
      } catch (e) {}
    }
  };
  window.CyberAudio = CyberAudio;

  // -------------------------------------------------------------
  // 2. Three.js Ambient 3D Cyber Particle & Constellation Field
  // -------------------------------------------------------------
  function initCyber3DBackground() {
    const canvas = document.getElementById('cyber3dCanvas');
    if (!canvas || typeof THREE === 'undefined') return;

    try {
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 1, 2000);
      camera.position.z = 700;

      const renderer = new THREE.WebGLRenderer({
        canvas: canvas,
        alpha: true,
        antialias: true,
        powerPreference: 'high-performance'
      });
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
      renderer.setSize(window.innerWidth, window.innerHeight);

      // Particle Geometry & Attributes
      const particleCount = window.innerWidth < 768 ? 90 : 160;
      const geometry = new THREE.BufferGeometry();
      const positions = new Float32Array(particleCount * 3);
      const velocities = [];
      const colors = new Float32Array(particleCount * 3);

      const colorPalette = [
        new THREE.Color(0x00e5ff), // Cyan
        new THREE.Color(0x00ff88), // Emerald
        new THREE.Color(0x3b82f6), // Blue
        new THREE.Color(0x8b5cf6)  // Purple
      ];

      for (let i = 0; i < particleCount; i++) {
        const i3 = i * 3;
        positions[i3] = (Math.random() - 0.5) * 1400;
        positions[i3 + 1] = (Math.random() - 0.5) * 1000;
        positions[i3 + 2] = (Math.random() - 0.5) * 600;

        velocities.push({
          x: (Math.random() - 0.5) * 0.4,
          y: (Math.random() - 0.5) * 0.4,
          z: (Math.random() - 0.5) * 0.2
        });

        const color = colorPalette[Math.floor(Math.random() * colorPalette.length)];
        colors[i3] = color.r;
        colors[i3 + 1] = color.g;
        colors[i3 + 2] = color.b;
      }

      geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

      // Circular particle texture generator
      const pCanvas = document.createElement('canvas');
      pCanvas.width = 32;
      pCanvas.height = 32;
      const pCtx = pCanvas.getContext('2d');
      const grad = pCtx.createRadialGradient(16, 16, 0, 16, 16, 16);
      grad.addColorStop(0, 'rgba(255,255,255,1)');
      grad.addColorStop(0.3, 'rgba(0,229,255,0.8)');
      grad.addColorStop(1, 'rgba(0,0,0,0)');
      pCtx.fillStyle = grad;
      pCtx.beginPath();
      pCtx.arc(16, 16, 16, 0, Math.PI * 2);
      pCtx.fill();
      const pTexture = new THREE.CanvasTexture(pCanvas);

      const pMaterial = new THREE.PointsMaterial({
        size: 9,
        vertexColors: true,
        map: pTexture,
        transparent: true,
        opacity: 0.75,
        blending: THREE.AdditiveBlending,
        depthWrite: false
      });

      const particleSystem = new THREE.Points(geometry, pMaterial);
      scene.add(particleSystem);

      // Connecting Constellation Lines
      const lineMaterial = new THREE.LineBasicMaterial({
        color: 0x00e5ff,
        transparent: true,
        opacity: 0.12,
        blending: THREE.AdditiveBlending,
        depthWrite: false
      });

      const lineGeometry = new THREE.BufferGeometry();
      const linePositions = new Float32Array(particleCount * particleCount * 6);
      lineGeometry.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));
      const lineMesh = new THREE.LineSegments(lineGeometry, lineMaterial);
      scene.add(lineMesh);

      // --- 3D Tron Perspective Cyber Horizon Floor & Ceiling Grids ---
      const gridGeo = new THREE.PlaneGeometry(2800, 2200, 40, 40);
      const gridMat = new THREE.MeshBasicMaterial({
        color: 0x00e5ff,
        wireframe: true,
        transparent: true,
        opacity: 0.18
      });
      const cyberGrid = new THREE.Mesh(gridGeo, gridMat);
      cyberGrid.rotation.x = -Math.PI / 2.3;
      cyberGrid.position.set(0, -320, 0);
      scene.add(cyberGrid);

      const ceilMat = new THREE.MeshBasicMaterial({
        color: 0x8b5cf6,
        wireframe: true,
        transparent: true,
        opacity: 0.09
      });
      const ceilingGrid = new THREE.Mesh(gridGeo, ceilMat);
      ceilingGrid.rotation.x = Math.PI / 2.3;
      ceilingGrid.position.set(0, 520, 0);
      scene.add(ceilingGrid);

      // --- Constellation of Floating Rotating 3D Polyhedra & Crystals ---
      const floatingShapesGroup = new THREE.Group();
      scene.add(floatingShapesGroup);

      const polyhedraDefs = [
        { geo: new THREE.IcosahedronGeometry(32, 0), color: 0x00e5ff, pos: [-460, 190, -180], rotSpd: [0.009, 0.012, 0.006] },
        { geo: new THREE.OctahedronGeometry(36, 0), color: 0x00ff88, pos: [510, -110, -140], rotSpd: [0.01, 0.008, 0.011] },
        { geo: new THREE.TorusGeometry(32, 2.5, 12, 40), color: 0x8b5cf6, pos: [-360, -210, -90], rotSpd: [0.012, 0.015, 0.007] },
        { geo: new THREE.DodecahedronGeometry(38, 0), color: 0x00e5ff, pos: [440, 250, -220], rotSpd: [0.007, 0.011, 0.013] },
        { geo: new THREE.TetrahedronGeometry(30, 0), color: 0x3b82f6, pos: [-580, -40, -280], rotSpd: [0.009, 0.013, 0.006] },
        { geo: new THREE.TorusGeometry(42, 2, 16, 50), color: 0x00ff88, pos: [600, 90, -260], rotSpd: [0.014, 0.007, 0.012] },
        { geo: new THREE.IcosahedronGeometry(24, 1), color: 0x8b5cf6, pos: [0, 310, -320], rotSpd: [0.006, 0.01, 0.014] },
        { geo: new THREE.OctahedronGeometry(28, 0), color: 0x00e5ff, pos: [-240, 270, -160], rotSpd: [0.011, 0.007, 0.009] },
        { geo: new THREE.TorusKnotGeometry(22, 4, 64, 8), color: 0x00e5ff, pos: [270, -250, -150], rotSpd: [0.013, 0.011, 0.008] }
      ];

      const floatingMeshes = [];
      polyhedraDefs.forEach((item, idx) => {
        const wireMaterial = new THREE.MeshBasicMaterial({
          color: item.color,
          wireframe: true,
          transparent: true,
          opacity: 0.6
        });
        const mesh = new THREE.Mesh(item.geo, wireMaterial);
        mesh.position.set(item.pos[0], item.pos[1], item.pos[2]);

        const innerMaterial = new THREE.MeshBasicMaterial({
          color: item.color,
          transparent: true,
          opacity: 0.09
        });
        const innerMesh = new THREE.Mesh(item.geo, innerMaterial);
        mesh.add(innerMesh);

        floatingShapesGroup.add(mesh);
        floatingMeshes.push({
          mesh: mesh,
          rotSpd: item.rotSpd,
          baseY: item.pos[1],
          phase: idx * 0.7
        });
      });

      // Mouse Parallax coordinates
      let mouseX = 0;
      let mouseY = 0;
      let targetX = 0;
      let targetY = 0;

      window.addEventListener('mousemove', (e) => {
        mouseX = (e.clientX - window.innerWidth / 2) * 0.35;
        mouseY = (e.clientY - window.innerHeight / 2) * 0.35;
      }, { passive: true });

      // Window resize
      window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
      });

      // Animation Loop
      function animate() {
        requestAnimationFrame(animate);

        const time = Date.now() * 0.001;

        // Animate floating 3D polyhedra & smooth floating bob
        floatingMeshes.forEach(item => {
          item.mesh.rotation.x += item.rotSpd[0];
          item.mesh.rotation.y += item.rotSpd[1];
          item.mesh.rotation.z += item.rotSpd[2];
          item.mesh.position.y = item.baseY + Math.sin(time + item.phase) * 14;
        });

        // Forward motion effect on cyber horizon grids
        cyberGrid.position.z = (time * 55) % 55;
        ceilingGrid.position.z = (time * 35) % 55;

        // Interpolate camera to mouse position
        targetX += (mouseX - targetX) * 0.03;
        targetY += (mouseY - targetY) * 0.03;
        camera.position.x = targetX;
        camera.position.y = -targetY + Math.sin(time * 0.6) * 10;
        camera.lookAt(scene.position);

        // Update particle positions
        const pos = geometry.attributes.position.array;
        let lineIdx = 0;
        const linePos = lineGeometry.attributes.position.array;
        const maxDist = 140;

        for (let i = 0; i < particleCount; i++) {
          const i3 = i * 3;
          pos[i3] += velocities[i].x;
          pos[i3 + 1] += velocities[i].y;
          pos[i3 + 2] += velocities[i].z;

          // Boundary bouncing
          if (pos[i3] < -700 || pos[i3] > 700) velocities[i].x *= -1;
          if (pos[i3 + 1] < -500 || pos[i3 + 1] > 500) velocities[i].y *= -1;
          if (pos[i3 + 2] < -300 || pos[i3 + 2] > 300) velocities[i].z *= -1;

          // Interconnecting lines for nearest neighbors
          for (let j = i + 1; j < particleCount; j++) {
            const j3 = j * 3;
            const dx = pos[i3] - pos[j3];
            const dy = pos[i3 + 1] - pos[j3 + 1];
            const dz = pos[i3 + 2] - pos[j3 + 2];
            const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);

            if (dist < maxDist && lineIdx < linePos.length - 6) {
              linePos[lineIdx++] = pos[i3];
              linePos[lineIdx++] = pos[i3 + 1];
              linePos[lineIdx++] = pos[i3 + 2];
              linePos[lineIdx++] = pos[j3];
              linePos[lineIdx++] = pos[j3 + 1];
              linePos[lineIdx++] = pos[j3 + 2];
            }
          }
        }

        geometry.attributes.position.needsUpdate = true;
        lineGeometry.setDrawRange(0, lineIdx / 3);
        lineGeometry.attributes.position.needsUpdate = true;

        renderer.render(scene, camera);
      }

      animate();
    } catch (err) {
      console.warn("3D WebGL Background init skipped:", err);
    }
  }

  // -------------------------------------------------------------
  // 3. Hero 3D Interactive Cyber Shield & Gyro Defense Core
  // -------------------------------------------------------------
  function initHero3DShield() {
    const container = document.getElementById('hero3dStage');
    if (!container || typeof THREE === 'undefined') return;

    try {
      const width = container.clientWidth || 420;
      const height = container.clientHeight || 420;

      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
      camera.position.z = 240;

      const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.setSize(width, height);
      renderer.outputEncoding = THREE.sRGBEncoding;
      container.appendChild(renderer.domElement);

      const mainGroup = new THREE.Group();
      scene.add(mainGroup);

      // A. Inner Energy Core (Glowing Icosahedron)
      const coreGeo = new THREE.IcosahedronGeometry(36, 1);
      const coreMat = new THREE.MeshPhongMaterial({
        color: 0x00e5ff,
        emissive: 0x005577,
        wireframe: true,
        wireframeLinewidth: 2,
        transparent: true,
        opacity: 0.85
      });
      const coreMesh = new THREE.Mesh(coreGeo, coreMat);
      mainGroup.add(coreMesh);

      // B. Inner Solid Pulsing Nucleus
      const nucleusGeo = new THREE.SphereGeometry(16, 24, 24);
      const nucleusMat = new THREE.MeshBasicMaterial({
        color: 0x00ff88,
        wireframe: false,
        transparent: true,
        opacity: 0.6
      });
      const nucleusMesh = new THREE.Mesh(nucleusGeo, nucleusMat);
      mainGroup.add(nucleusMesh);

      // C. Holographic Shield Polyhedron (Dodecahedron with translucent faces)
      const shieldGeo = new THREE.DodecahedronGeometry(58, 1);
      const shieldMat = new THREE.MeshPhysicalMaterial({
        color: 0x00e5ff,
        metalness: 0.2,
        roughness: 0.1,
        transmission: 0.85,
        transparent: true,
        opacity: 0.35,
        wireframe: false
      });
      const shieldMesh = new THREE.Mesh(shieldGeo, shieldMat);
      mainGroup.add(shieldMesh);

      // D. Shield Wireframe Overlay
      const wireMat = new THREE.MeshBasicMaterial({
        color: 0x00e5ff,
        wireframe: true,
        transparent: true,
        opacity: 0.4
      });
      const wireMesh = new THREE.Mesh(shieldGeo, wireMat);
      mainGroup.add(wireMesh);

      // E. Rotating Gyro Orbital Rings
      const ringGeo1 = new THREE.TorusGeometry(72, 1.2, 16, 80);
      const ringMat1 = new THREE.MeshBasicMaterial({
        color: 0x00e5ff,
        transparent: true,
        opacity: 0.7
      });
      const ringMesh1 = new THREE.Mesh(ringGeo1, ringMat1);
      ringMesh1.rotation.x = Math.PI / 3;
      mainGroup.add(ringMesh1);

      const ringGeo2 = new THREE.TorusGeometry(84, 1.2, 16, 80);
      const ringMat2 = new THREE.MeshBasicMaterial({
        color: 0x8b5cf6,
        transparent: true,
        opacity: 0.6
      });
      const ringMesh2 = new THREE.Mesh(ringGeo2, ringMat2);
      ringMesh2.rotation.y = Math.PI / 4;
      mainGroup.add(ringMesh2);

      const ringGeo3 = new THREE.TorusGeometry(96, 1.2, 16, 80);
      const ringMat3 = new THREE.MeshBasicMaterial({
        color: 0x00ff88,
        transparent: true,
        opacity: 0.5
      });
      const ringMesh3 = new THREE.Mesh(ringGeo3, ringMat3);
      ringMesh3.rotation.z = Math.PI / 6;
      mainGroup.add(ringMesh3);

      // F. Orbiting Satellite Nodes
      const nodeCount = 6;
      const nodeGroup = new THREE.Group();
      mainGroup.add(nodeGroup);
      for (let i = 0; i < nodeCount; i++) {
        const nGeo = new THREE.OctahedronGeometry(4);
        const nMat = new THREE.MeshBasicMaterial({
          color: i % 2 === 0 ? 0x00e5ff : 0x00ff88,
          wireframe: true
        });
        const nMesh = new THREE.Mesh(nGeo, nMat);
        const angle = (i / nodeCount) * Math.PI * 2;
        nMesh.position.set(Math.cos(angle) * 78, Math.sin(angle) * 78, (i % 2 === 0 ? 1 : -1) * 20);
        nodeGroup.add(nMesh);
      }

      // G. Lights
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
      scene.add(ambientLight);

      const pointLight1 = new THREE.PointLight(0x00e5ff, 2, 300);
      pointLight1.position.set(60, 60, 80);
      scene.add(pointLight1);

      const pointLight2 = new THREE.PointLight(0x8b5cf6, 2, 300);
      pointLight2.position.set(-60, -60, -80);
      scene.add(pointLight2);

      // Interactive mouse rotation
      let mouseOver = false;
      let rotTargetX = 0;
      let rotTargetY = 0;
      let isDragging = false;
      let prevMousePos = { x: 0, y: 0 };

      container.addEventListener('mouseenter', () => { mouseOver = true; });
      container.addEventListener('mouseleave', () => { mouseOver = false; isDragging = false; });

      container.addEventListener('mousedown', (e) => {
        isDragging = true;
        prevMousePos = { x: e.clientX, y: e.clientY };
        CyberAudio.playBeep(920, 'sine', 0.05, 0.06);
      });

      window.addEventListener('mouseup', () => { isDragging = false; });

      window.addEventListener('mousemove', (e) => {
        const rect = container.getBoundingClientRect();
        if (isDragging) {
          const deltaX = e.clientX - prevMousePos.x;
          const deltaY = e.clientY - prevMousePos.y;
          mainGroup.rotation.y += deltaX * 0.01;
          mainGroup.rotation.x += deltaY * 0.01;
          prevMousePos = { x: e.clientX, y: e.clientY };
        } else if (mouseOver) {
          const relX = (e.clientX - rect.left) / rect.width - 0.5;
          const relY = (e.clientY - rect.top) / rect.height - 0.5;
          rotTargetY = relX * 1.5;
          rotTargetX = -relY * 1.5;
        }
      });

      // Pulse trigger on click
      container.addEventListener('click', () => {
        pulseCore();
      });

      let pulseScale = 1;
      function pulseCore() {
        pulseScale = 1.35;
        CyberAudio.playBeep(1200, 'triangle', 0.15, 0.1);
      }

      // Responsive resize
      window.addEventListener('resize', () => {
        const w = container.clientWidth;
        const h = container.clientHeight;
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
      });

      // Animation Loop
      let clock = new THREE.Clock();
      function animateHero() {
        requestAnimationFrame(animateHero);
        const delta = clock.getDelta();
        const time = clock.getElapsedTime();

        // Autonomous idle rotation
        if (!isDragging) {
          mainGroup.rotation.y += (rotTargetY - mainGroup.rotation.y) * 0.05 + 0.008;
          mainGroup.rotation.x += (rotTargetX - mainGroup.rotation.x) * 0.05 + 0.003;
        }

        // Internal counter-rotations
        coreMesh.rotation.x -= 0.015;
        coreMesh.rotation.y -= 0.02;
        shieldMesh.rotation.y += 0.01;
        wireMesh.rotation.y += 0.01;

        ringMesh1.rotation.z += 0.015;
        ringMesh2.rotation.x += 0.012;
        ringMesh3.rotation.y += 0.018;

        nodeGroup.rotation.z += 0.02;

        // Breathing & Pulsing
        pulseScale += (1.0 - pulseScale) * 0.08;
        const breath = 1.0 + Math.sin(time * 3) * 0.05;
        coreMesh.scale.set(breath * pulseScale, breath * pulseScale, breath * pulseScale);
        nucleusMesh.scale.set(breath * 1.1 * pulseScale, breath * 1.1 * pulseScale, breath * 1.1 * pulseScale);

        renderer.render(scene, camera);
      }

      animateHero();
    } catch (err) {
      console.warn("Hero 3D Stage init skipped:", err);
    }
  }

  // -------------------------------------------------------------
  // 4. Dashboard Interactive 3D Cyber Threat Globe
  // -------------------------------------------------------------
  function initDashboard3DGlobe() {
    const container = document.getElementById('dashboard3dGlobe');
    if (!container || typeof THREE === 'undefined') return;

    try {
      const width = container.clientWidth || 360;
      const height = container.clientHeight || 280;

      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
      camera.position.z = 190;

      const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.setSize(width, height);
      container.appendChild(renderer.domElement);

      const globeGroup = new THREE.Group();
      scene.add(globeGroup);

      // Globe Wireframe Sphere
      const sphereGeo = new THREE.SphereGeometry(60, 24, 24);
      const sphereMat = new THREE.MeshBasicMaterial({
        color: 0x00e5ff,
        wireframe: true,
        transparent: true,
        opacity: 0.25
      });
      const globeMesh = new THREE.Mesh(sphereGeo, sphereMat);
      globeGroup.add(globeMesh);

      // Inner Dark Core
      const innerGeo = new THREE.SphereGeometry(58.5, 32, 32);
      const innerMat = new THREE.MeshBasicMaterial({
        color: 0x050811,
        transparent: true,
        opacity: 0.9
      });
      const innerMesh = new THREE.Mesh(innerGeo, innerMat);
      globeGroup.add(innerMesh);

      // Latitude/Longitude Grid rings
      const latRingGeo = new THREE.RingGeometry(59.8, 60.2, 64);
      const latRingMat = new THREE.MeshBasicMaterial({
        color: 0x00ff88,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.4
      });
      const equator = new THREE.Mesh(latRingGeo, latRingMat);
      equator.rotation.x = Math.PI / 2;
      globeGroup.add(equator);

      // Simulated Cyber Threat Radar Nodes on Globe Surface
      const threatPoints = [
        { lat: 20.5937, lon: 78.9629, label: "India Cyber Command", color: 0x00ff88 }, // India
        { lat: 28.6139, lon: 77.2090, label: "Delhi CERT-In Node", color: 0x00e5ff },
        { lat: 19.0760, lon: 72.8777, label: "Mumbai Cyber Cell", color: 0x00e5ff },
        { lat: 12.9716, lon: 77.5946, label: "Bengaluru Tech Hub", color: 0x00e5ff },
        { lat: 26.9124, lon: 75.7873, label: "Jaipur Cyber Defense", color: 0x00ff88 },
        { lat: 37.7749, lon: -122.4194, label: "Global Gateway US", color: 0x8b5cf6 },
        { lat: 51.5074, lon: -0.1278, label: "Global Gateway UK", color: 0x8b5cf6 },
        { lat: 1.3521, lon: 103.8198, label: "APAC Gateway SG", color: 0x8b5cf6 },
        { lat: -25.2744, lon: 133.7751, label: "Oceania Node", color: 0x8b5cf6 }
      ];

      function latLonToVector3(lat, lon, radius) {
        const phi = (90 - lat) * (Math.PI / 180);
        const theta = (lon + 180) * (Math.PI / 180);
        return new THREE.Vector3(
          -(radius * Math.sin(phi) * Math.cos(theta)),
          radius * Math.cos(phi),
          radius * Math.sin(phi) * Math.sin(theta)
        );
      }

      threatPoints.forEach(pt => {
        const pos = latLonToVector3(pt.lat, pt.lon, 61);
        const ptGeo = new THREE.SphereGeometry(2, 8, 8);
        const ptMat = new THREE.MeshBasicMaterial({ color: pt.color });
        const ptMesh = new THREE.Mesh(ptGeo, ptMat);
        ptMesh.position.copy(pos);
        globeGroup.add(ptMesh);

        // Radar ping ring
        const ringGeo = new THREE.RingGeometry(2.5, 3.5, 16);
        const ringMat = new THREE.MeshBasicMaterial({
          color: pt.color,
          side: THREE.DoubleSide,
          transparent: true,
          opacity: 0.8
        });
        const pingMesh = new THREE.Mesh(ringGeo, ringMat);
        pingMesh.position.copy(pos.clone().multiplyScalar(1.02));
        pingMesh.lookAt(new THREE.Vector3(0, 0, 0));
        globeGroup.add(pingMesh);
      });

      // Connecting Cyber Flight Arcs between India and Global nodes
      const indiaPos = latLonToVector3(20.5937, 78.9629, 61);
      [
        latLonToVector3(37.7749, -122.4194, 61),
        latLonToVector3(51.5074, -0.1278, 61),
        latLonToVector3(1.3521, 103.8198, 61)
      ].forEach(dest => {
        const mid = indiaPos.clone().lerp(dest, 0.5).normalize().multiplyScalar(78);
        const curve = new THREE.QuadraticBezierCurve3(indiaPos, mid, dest);
        const arcPoints = curve.getPoints(30);
        const arcGeo = new THREE.BufferGeometry().setFromPoints(arcPoints);
        const arcMat = new THREE.LineBasicMaterial({
          color: 0x00e5ff,
          transparent: true,
          opacity: 0.55
        });
        const arcLine = new THREE.Line(arcGeo, arcMat);
        globeGroup.add(arcLine);
      });

      // Initial orientation focusing near India
      globeGroup.rotation.y = -1.2;
      globeGroup.rotation.x = 0.3;

      let isDragging = false;
      let prevMousePos = { x: 0, y: 0 };

      container.addEventListener('mousedown', (e) => {
        isDragging = true;
        prevMousePos = { x: e.clientX, y: e.clientY };
      });
      window.addEventListener('mouseup', () => { isDragging = false; });
      window.addEventListener('mousemove', (e) => {
        if (isDragging) {
          const dx = e.clientX - prevMousePos.x;
          const dy = e.clientY - prevMousePos.y;
          globeGroup.rotation.y += dx * 0.01;
          globeGroup.rotation.x += dy * 0.01;
          prevMousePos = { x: e.clientX, y: e.clientY };
        }
      });

      function animateGlobe() {
        requestAnimationFrame(animateGlobe);
        if (!isDragging) {
          globeGroup.rotation.y += 0.005;
        }
        renderer.render(scene, camera);
      }
      animateGlobe();

      window.addEventListener('resize', () => {
        const w = container.clientWidth;
        const h = container.clientHeight;
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
      });
    } catch (e) {
      console.warn("Dashboard 3D Globe init skipped:", e);
    }
  }

  // -------------------------------------------------------------
  // 5. Zero-Dependency 3D Perspective Card Tilt & Dynamic Glare
  // -------------------------------------------------------------
  function init3DCardTilt() {
    // Select cards for 3D perspective tilt
    const tiltCards = document.querySelectorAll(
      '.cyber-card, .stat-card, .soc-stat-tile, .feature-card, .threat-card, .threat-item, .quiz-card, .news-card, .sample-pill, .vesper-stats, .soc-command-hero'
    );

    tiltCards.forEach(card => {
      // Create glare overlay element if not present
      let glare = card.querySelector('.cyber-glare');
      if (!glare && !card.classList.contains('sample-pill')) {
        glare = document.createElement('div');
        glare.className = 'cyber-glare';
        card.appendChild(glare);
      }

      card.addEventListener('mouseenter', () => {
        card.style.transition = 'transform 0.12s ease-out, box-shadow 0.25s ease';
        if (glare) glare.style.opacity = '1';
      });

      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const cardWidth = rect.width;
        const cardHeight = rect.height;

        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;

        // Calculate rotation (-14deg to +14deg)
        const rotY = ((mouseX / cardWidth) - 0.5) * 18;
        const rotX = -(((mouseY / cardHeight) - 0.5) * 18);

        card.style.transform = `perspective(1000px) rotateX(${rotX.toFixed(2)}deg) rotateY(${rotY.toFixed(2)}deg) translateZ(12px)`;

        // Move dynamic specular glare
        if (glare) {
          const percentX = (mouseX / cardWidth) * 100;
          const percentY = (mouseY / cardHeight) * 100;
          glare.style.background = `radial-gradient(circle at ${percentX}% ${percentY}%, rgba(0, 229, 255, 0.24) 0%, rgba(255, 255, 255, 0.08) 28%, transparent 65%)`;
        }
      });

      card.addEventListener('mouseleave', () => {
        card.style.transition = 'transform 0.45s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.3s ease';
        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0px)';
        if (glare) glare.style.opacity = '0';
      });
    });
  }

  // -------------------------------------------------------------
  // 6. 3D Laser Grid Scanner Visualizer (Triggered on scan)
  // -------------------------------------------------------------
  function trigger3DLaserSweep(containerId = 'scannerSection') {
    const section = document.getElementById(containerId);
    if (!section) return;

    let laser = section.querySelector('.cyber-3d-laser-grid');
    if (!laser) {
      laser = document.createElement('div');
      laser.className = 'cyber-3d-laser-grid';
      laser.innerHTML = `
        <div class="laser-beam"></div>
        <div class="laser-mesh-lines"></div>
      `;
      section.appendChild(laser);
    }

    laser.classList.add('scanning');
    CyberAudio.playScanLaser();

    setTimeout(() => {
      laser.classList.remove('scanning');
    }, 2000);
  }
  window.trigger3DLaserSweep = trigger3DLaserSweep;

  // -------------------------------------------------------------
  // 7. Initialize All Cyber 3D Modules on DOM Ready
  // -------------------------------------------------------------
  document.addEventListener('DOMContentLoaded', () => {
    CyberAudio.init();
    initCyber3DBackground();
    initHero3DShield();
    initDashboard3DGlobe();
    init3DCardTilt();

    // Attach SFX to buttons with .btn or .sample-pill
    document.querySelectorAll('.btn, .type-pill, .sample-pill').forEach(btn => {
      btn.addEventListener('click', () => {
        CyberAudio.playBeep(800, 'sine', 0.04, 0.06);
      });
    });
  });

})();
