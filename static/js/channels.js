// Variables globales
let allChannels = [];
let currentCategory = 'all';

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    loadAllChannels();
});

// Charger toutes les chaînes
async function loadAllChannels() {
    const loading = document.getElementById('loading');
    const channelsGrid = document.getElementById('channelsGrid');
    
    loading.style.display = 'block';
    
    try {
        const response = await fetch('/api/channels');
        
        if (!response.ok) {
            throw new Error('Erreur lors du chargement des chaînes');
        }
        
        allChannels = await response.json();
        displayChannels(allChannels);
        
    } catch (error) {
        console.error('Erreur:', error);
        channelsGrid.innerHTML = `
            <div class="error-message" style="text-align: center; color: white; padding: 2rem; grid-column: 1/-1;">
                <i class="fas fa-exclamation-triangle" style="font-size: 3rem; margin-bottom: 1rem;"></i>
                <p>عذراً، حدث خطأ أثناء تحميل القنوات</p>
                <button onclick="loadAllChannels()" style="margin-top: 1rem; padding: 0.75rem 2rem; background: white; color: #667eea; border: none; border-radius: 25px; cursor: pointer; font-weight: 600;">
                    <i class="fas fa-redo"></i> إعادة المحاولة
                </button>
            </div>
        `;
    } finally {
        loading.style.display = 'none';
    }
}

// Afficher les chaînes
function displayChannels(channels) {
    const channelsGrid = document.getElementById('channelsGrid');
    
    if (!channels || channels.length === 0) {
        channelsGrid.innerHTML = `
            <div style="text-align: center; color: white; padding: 3rem; grid-column: 1/-1;">
                <i class="fas fa-tv" style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                <h3>لا توجد قنوات متاحة</h3>
            </div>
        `;
        return;
    }
    
    let html = '';
    
    channels.forEach(channel => {
        html += createChannelCard(channel);
    });
    
    channelsGrid.innerHTML = html;
}

// Créer une carte de chaîne
function createChannelCard(channel) {
    const categoryIcons = {
        'bein': 'fa-futbol',
        'dazn': 'fa-video',
        'espn': 'fa-basketball-ball',
        'elevendazn': 'fa-tv',
        'sky': 'fa-satellite-dish',
        'premierleague': 'fa-trophy',
        'roshnleague': 'fa-medal',
        'SeriaA': 'fa-flag',
        'generalsports': 'fa-running',
        'mbc': 'fa-film'
    };
    
    const icon = categoryIcons[channel.category] || 'fa-tv';
    
    return `
        <div class="channel-card" onclick="playChannel('${encodeURIComponent(JSON.stringify(channel))}')">
            <div class="channel-icon">
                <i class="fas ${icon}"></i>
            </div>
            <div class="channel-name">${channel.name}</div>
            <div class="channel-category">${channel.category}</div>
            <button class="watch-btn" style="margin-top: 1rem; width: 100%;" onclick="playChannel('${encodeURIComponent(JSON.stringify(channel))}'); event.stopPropagation();">
                <i class="fas fa-play"></i> مشاهدة
            </button>
        </div>
    `;
}

// Jouer une chaîne
function playChannel(channelData) {
    try {
        const channel = JSON.parse(decodeURIComponent(channelData));
        
        // Mettre à jour le titre
        document.getElementById('currentStreamTitle').textContent = channel.name;
        document.getElementById('currentStreamDescription').textContent = 
            `قناة ${channel.category} - بث مباشر`;
        
        // Charger le stream
        const videoPlayer = document.getElementById('videoPlayer');
        
        // Afficher un loader d'abord
        videoPlayer.innerHTML = `
            <div class="video-placeholder">
                <i class="fas fa-spinner fa-spin" style="font-size: 3rem; margin-bottom: 1rem;"></i>
                <p>جاري تحميل البث...</p>
            </div>
        `;
        
        // Après un court délai, charger le stream
        setTimeout(() => {
            // Créer l'élément vidéo
            videoPlayer.innerHTML = `
                <video id="hlsPlayer" controls autoplay muted style="width: 100%; height: 100%; background: #000;">
                    Votre navigateur ne supporte pas la lecture vidéo
                </video>
            `;
            
            const video = document.getElementById('hlsPlayer');
            
            // Utiliser le proxy pour les chaînes Eleven et Sky
            const needsProxy = (channel.category === 'elevendazn' || channel.category === 'sky');
            const streamUrl = needsProxy ? `/proxy/stream?url=${encodeURIComponent(channel.url)}` : channel.url;
            
            // Vérifier si c'est un flux m3u8 (HLS)
            if (channel.url.includes('.m3u8')) {
                // Utiliser hls.js si disponible
                if (typeof Hls !== 'undefined' && Hls.isSupported()) {
                    const hls = new Hls({
                        enableWorker: true,
                        lowLatencyMode: true,
                        backBufferLength: 90,
                        xhrSetup: function(xhr, url) {
                            // Pas besoin de configuration spéciale, le proxy gère tout
                        }
                    });
                    
                    hls.loadSource(streamUrl);
                    hls.attachMedia(video);
                    
                    hls.on(Hls.Events.MANIFEST_PARSED, function() {
                        console.log('Manifest chargé, démarrage de la lecture...');
                        video.play().catch(e => {
                            console.log('Autoplay bloqué, cliquez pour lire:', e);
                            // Créer un bouton de lecture
                            const playBtn = document.createElement('div');
                            playBtn.style.cssText = 'position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(255,255,255,0.9); padding: 20px 40px; border-radius: 50px; cursor: pointer; z-index: 100;';
                            playBtn.innerHTML = '<i class="fas fa-play" style="font-size: 2rem; color: #667eea;"></i>';
                            playBtn.onclick = () => {
                                video.play();
                                playBtn.remove();
                            };
                            videoPlayer.style.position = 'relative';
                            videoPlayer.appendChild(playBtn);
                        });
                    });
                    
                    hls.on(Hls.Events.ERROR, function(event, data) {
                        console.error('Erreur HLS:', data);
                        if (data.fatal) {
                            switch(data.type) {
                                case Hls.ErrorTypes.NETWORK_ERROR:
                                    console.log('Erreur réseau, tentative de récupération...');
                                    hls.startLoad();
                                    break;
                                case Hls.ErrorTypes.MEDIA_ERROR:
                                    console.log('Erreur média, tentative de récupération...');
                                    hls.recoverMediaError();
                                    break;
                                default:
                                    videoPlayer.innerHTML = `
                                        <div class="video-placeholder">
                                            <i class="fas fa-exclamation-circle" style="font-size: 3rem; margin-bottom: 1rem; color: #ff3366;"></i>
                                            <p>عذراً، لا يمكن تشغيل هذه القناة</p>
                                            <p style="font-size: 0.85rem; margin-top: 1rem; opacity: 0.7;">خطأ في تحميل البث</p>
                                        </div>
                                    `;
                                    break;
                            }
                        }
                    });
                } 
                // Safari supporte nativement HLS
                else if (video.canPlayType('application/vnd.apple.mpegurl')) {
                    video.src = channel.url;
                    video.play().catch(e => console.log('Erreur de lecture:', e));
                } 
                else {
                    videoPlayer.innerHTML = `
                        <div class="video-placeholder">
                            <i class="fas fa-exclamation-circle" style="font-size: 3rem; margin-bottom: 1rem; color: #ff3366;"></i>
                            <p>عذراً، متصفحك لا يدعم تشغيل هذا النوع من البث</p>
                            <p style="font-size: 0.85rem; margin-top: 1rem; opacity: 0.7;">استخدم متصفح حديث أو VLC</p>
                        </div>
                    `;
                }
            } else {
                // Pour les URLs non-m3u8, essayer la lecture directe
                video.src = channel.url;
                video.play().catch(e => {
                    console.log('Erreur de lecture:', e);
                    videoPlayer.innerHTML = `
                        <div class="video-placeholder">
                            <i class="fas fa-exclamation-circle" style="font-size: 3rem; margin-bottom: 1rem; color: #ff3366;"></i>
                            <p>عذراً، لا يمكن تشغيل هذه القناة</p>
                            <p style="font-size: 0.85rem; margin-top: 1rem; opacity: 0.7;">الرابط غير متاح أو محمي</p>
                        </div>
                    `;
                });
            }
        }, 500);
        
        // Scroll vers le lecteur
        document.querySelector('.video-player-section').scrollIntoView({ behavior: 'smooth' });
        
    } catch (error) {
        console.error('Erreur lors de la lecture de la chaîne:', error);
        const videoPlayer = document.getElementById('videoPlayer');
        videoPlayer.innerHTML = `
            <div class="video-placeholder">
                <i class="fas fa-times-circle" style="font-size: 3rem; margin-bottom: 1rem; color: #ff3366;"></i>
                <p>عذراً، حدث خطأ أثناء تحميل القناة</p>
            </div>
        `;
    }
}

// Rechercher des chaînes
function searchChannels() {
    const searchInput = document.getElementById('searchInput');
    const searchTerm = searchInput.value.toLowerCase().trim();
    
    if (!searchTerm) {
        // Si la recherche est vide, afficher toutes les chaînes de la catégorie actuelle
        filterCategory(currentCategory);
        return;
    }
    
    // Filtrer les chaînes par nom
    const filteredChannels = allChannels.filter(channel => 
        channel.name.toLowerCase().includes(searchTerm) ||
        channel.category.toLowerCase().includes(searchTerm)
    );
    
    displayChannels(filteredChannels);
}

// Filtrer par catégorie
function filterCategory(category) {
    currentCategory = category;
    
    // Mettre à jour les boutons
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Filtrer les chaînes
    let filteredChannels = allChannels;
    
    if (category !== 'all') {
        filteredChannels = allChannels.filter(channel => 
            channel.category.toLowerCase() === category.toLowerCase()
        );
    }
    
    // Réinitialiser la barre de recherche
    document.getElementById('searchInput').value = '';
    
    displayChannels(filteredChannels);
}
