// Variables globales
let currentDate = new Date();
let allMatches = [];
let currentFilter = 'all';

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    loadTodayMatches();
    loadPopularChannels();
    updateDateDisplay();
    
    // Rafraîchir les matchs toutes les 2 minutes
    setInterval(loadTodayMatches, 120000);
});

// Charger les matchs du jour
async function loadTodayMatches() {
    const loading = document.getElementById('loading');
    const matchesContainer = document.getElementById('matchesContainer');
    
    loading.style.display = 'block';
    
    try {
        const dateStr = formatDate(currentDate);
        const response = await fetch(`/api/matches/date/${dateStr}`);
        
        if (!response.ok) {
            throw new Error('Erreur lors du chargement des matchs');
        }
        
        allMatches = await response.json();
        displayMatches(allMatches);
        
    } catch (error) {
        console.error('Erreur:', error);
        matchesContainer.innerHTML = `
            <div class="error-message" style="text-align: center; color: white; padding: 2rem;">
                <i class="fas fa-exclamation-triangle" style="font-size: 3rem; margin-bottom: 1rem;"></i>
                <p>عذراً، حدث خطأ أثناء تحميل المباريات</p>
                <button onclick="loadTodayMatches()" style="margin-top: 1rem; padding: 0.75rem 2rem; background: white; color: #667eea; border: none; border-radius: 25px; cursor: pointer; font-weight: 600;">
                    <i class="fas fa-redo"></i> إعادة المحاولة
                </button>
            </div>
        `;
    } finally {
        loading.style.display = 'none';
    }
}

// Afficher les matchs
function displayMatches(matches) {
    const matchesContainer = document.getElementById('matchesContainer');
    
    if (!matches || matches.length === 0) {
        matchesContainer.innerHTML = `
            <div style="text-align: center; color: white; padding: 3rem;">
                <i class="fas fa-calendar-times" style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                <h3>لا توجد مباريات في هذا التاريخ</h3>
                <p style="margin-top: 1rem; opacity: 0.8;">جرب تاريخاً آخر</p>
            </div>
        `;
        return;
    }
    
    // Filtrer les matchs selon le filtre actuel
    let filteredMatches = matches;
    if (currentFilter === 'live') {
        filteredMatches = matches.filter(m => m.is_live);
    } else if (currentFilter === 'upcoming') {
        filteredMatches = matches.filter(m => m.status === 'Scheduled');
    } else if (currentFilter === 'finished') {
        filteredMatches = matches.filter(m => m.status === 'Finished');
    }
    
    if (filteredMatches.length === 0) {
        matchesContainer.innerHTML = `
            <div style="text-align: center; color: white; padding: 3rem;">
                <i class="fas fa-filter" style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                <h3>لا توجد مباريات ${getFilterText(currentFilter)}</h3>
            </div>
        `;
        return;
    }
    
    // Grouper les matchs par compétition
    const groupedMatches = groupByCompetition(filteredMatches);
    
    let html = '';
    
    for (const [competition, competitionMatches] of Object.entries(groupedMatches)) {
        html += `
            <div class="competition-group" style="margin-bottom: 2rem;">
                <h3 style="color: white; margin-bottom: 1rem; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px;">
                    <i class="fas fa-trophy"></i> ${competition}
                </h3>
                <div style="display: grid; gap: 1.5rem;">
        `;
        
        competitionMatches.forEach(match => {
            html += createMatchCard(match);
        });
        
        html += `
                </div>
            </div>
        `;
    }
    
    matchesContainer.innerHTML = html;
}

// Créer une carte de match
function createMatchCard(match) {
    const statusClass = match.is_live ? 'live' : '';
    const statusText = getStatusText(match.status, match.is_live);
    const statusIcon = match.is_live ? '<i class="fas fa-circle"></i>' : '<i class="fas fa-clock"></i>';
    
    // Logo de l'équipe à domicile
    const homeLogo = match.home_logo ? 
        `<img src="${match.home_logo}" alt="${match.home_team}" class="team-logo-img" onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
         <i class="fas fa-shield-alt team-logo-fallback" style="display:none; font-size: 3rem; color: #667eea;"></i>` :
        `<i class="fas fa-shield-alt" style="font-size: 3rem; color: #667eea;"></i>`;
    
    // Logo de l'équipe à l'extérieur
    const awayLogo = match.away_logo ? 
        `<img src="${match.away_logo}" alt="${match.away_team}" class="team-logo-img" onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
         <i class="fas fa-shield-alt team-logo-fallback" style="display:none; font-size: 3rem; color: #764ba2;"></i>` :
        `<i class="fas fa-shield-alt" style="font-size: 3rem; color: #764ba2;"></i>`;
    
    // Logo de la compétition
    const competitionLogo = match.competition_logo ? 
        `<img src="${match.competition_logo}" alt="${match.competition}" class="competition-logo"> ` : 
        '<i class="fas fa-trophy"></i> ';
    
    // Chaînes de diffusion
    let channelsHtml = '';
    if (match.channels && match.channels.length > 0) {
        channelsHtml = '<div class="broadcast-channels">';
        match.channels.forEach(channel => {
            if (channel.logo) {
                channelsHtml += `<img src="${channel.logo}" alt="${channel.name}" title="${channel.name}" class="channel-logo">`;
            } else {
                channelsHtml += `<span class="channel-name">${channel.name}</span>`;
            }
        });
        channelsHtml += '</div>';
    }
    
    return `
        <div class="match-card" onclick="playMatch('${encodeURIComponent(JSON.stringify(match))}')">
            <div class="match-header">
                <div class="match-competition">
                    ${competitionLogo}${match.competition}
                </div>
                <div class="match-status ${statusClass}">
                    ${statusIcon} ${statusText}
                </div>
            </div>
            <div class="match-body">
                <div class="team">
                    <div class="team-logo">
                        ${homeLogo}
                    </div>
                    <div class="team-name">${match.home_team}</div>
                </div>
                <div class="match-score">
                    <div class="score">${match.score}</div>
                    <div class="match-time">${match.time}</div>
                </div>
                <div class="team">
                    <div class="team-logo">
                        ${awayLogo}
                    </div>
                    <div class="team-name">${match.away_team}</div>
                </div>
            </div>
            <div class="match-footer">
                <div class="match-footer-content">
                    ${channelsHtml}
                    ${channelsHtml ? '' : `<span style="color: #666; font-size: 0.85rem;">
                        <i class="fas fa-info-circle"></i> ${match.source || 'Source inconnue'}
                    </span>`}
                </div>
                <button class="watch-btn" onclick="playMatch('${encodeURIComponent(JSON.stringify(match))}'); event.stopPropagation();">
                    <i class="fas fa-play"></i> مشاهدة
                </button>
            </div>
        </div>
    `;
}

// Jouer un match
function playMatch(matchData) {
    try {
        const match = JSON.parse(decodeURIComponent(matchData));
        
        // Mettre à jour le titre
        document.getElementById('currentStreamTitle').textContent = 
            `${match.home_team} vs ${match.away_team}`;
        document.getElementById('currentStreamDescription').textContent = 
            `${match.competition} - ${match.time}`;
        
        // Chercher des streams disponibles
        searchAndPlayStream(match);
        
        // Scroll vers le lecteur
        document.querySelector('.video-player-section').scrollIntoView({ behavior: 'smooth' });
        
    } catch (error) {
        console.error('Erreur lors de la lecture du match:', error);
        alert('عذراً، حدث خطأ أثناء تحميل المباراة');
    }
}

// Chercher et jouer un stream
async function searchAndPlayStream(match) {
    const videoPlayer = document.getElementById('videoPlayer');
    
    // Pour l'instant, afficher un message
    videoPlayer.innerHTML = `
        <div class="video-placeholder">
            <i class="fas fa-search" style="font-size: 3rem; margin-bottom: 1rem;"></i>
            <p>البحث عن البث المباشر...</p>
            <p style="font-size: 0.9rem; margin-top: 1rem; opacity: 0.8;">
                ${match.home_team} vs ${match.away_team}
            </p>
        </div>
    `;
    
    // Ici, vous pouvez ajouter la logique pour chercher les streams
    // Par exemple, chercher dans les chaînes qui diffusent ce match
    
    setTimeout(() => {
        videoPlayer.innerHTML = `
            <div class="video-placeholder">
                <i class="fas fa-tv"></i>
                <p>اختر قناة من القائمة أدناه</p>
                <p style="font-size: 0.9rem; margin-top: 1rem; opacity: 0.8;">
                    القنوات التي قد تبث هذه المباراة
                </p>
            </div>
        `;
    }, 2000);
}

// Charger les chaînes populaires
async function loadPopularChannels() {
    try {
        const response = await fetch('/api/channels');
        
        if (!response.ok) {
            throw new Error('Erreur lors du chargement des chaînes');
        }
        
        const channels = await response.json();
        displayPopularChannels(channels.slice(0, 12)); // Afficher les 12 premières
        
    } catch (error) {
        console.error('Erreur:', error);
    }
}

// Afficher les chaînes populaires
function displayPopularChannels(channels) {
    const channelsContainer = document.getElementById('channelsContainer');
    
    if (!channels || channels.length === 0) {
        return;
    }
    
    let html = '';
    
    channels.forEach(channel => {
        html += `
            <div class="channel-card" onclick="playChannel('${encodeURIComponent(JSON.stringify(channel))}')">
                <div class="channel-icon">
                    <i class="fas fa-tv"></i>
                </div>
                <div class="channel-name">${channel.name}</div>
                <div class="channel-category">${channel.category}</div>
            </div>
        `;
    });
    
    channelsContainer.innerHTML = html;
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

// Changer la date
function changeDate(days) {
    currentDate.setDate(currentDate.getDate() + days);
    updateDateDisplay();
    loadTodayMatches();
}

// Mettre à jour l'affichage de la date
function updateDateDisplay() {
    const dateElement = document.getElementById('currentDate');
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    const selectedDate = new Date(currentDate);
    selectedDate.setHours(0, 0, 0, 0);
    
    if (selectedDate.getTime() === today.getTime()) {
        dateElement.textContent = 'اليوم';
    } else {
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        dateElement.textContent = currentDate.toLocaleDateString('ar-EG', options);
    }
}

// Filtrer les matchs
function filterMatches(filter) {
    currentFilter = filter;
    
    // Mettre à jour les boutons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Réafficher les matchs avec le filtre
    displayMatches(allMatches);
}

// Fonctions utilitaires
function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

function groupByCompetition(matches) {
    const grouped = {};
    
    matches.forEach(match => {
        const competition = match.competition || 'Autres';
        if (!grouped[competition]) {
            grouped[competition] = [];
        }
        grouped[competition].push(match);
    });
    
    return grouped;
}

function getStatusText(status, isLive) {
    if (isLive) return 'مباشر الآن';
    
    const statusMap = {
        'Scheduled': 'لم تبدأ',
        'Live': 'مباشر',
        'Finished': 'انتهت',
        'Half Time': 'استراحة',
        'Postponed': 'مؤجلة',
        'Cancelled': 'ملغاة'
    };
    
    return statusMap[status] || status;
}

function getFilterText(filter) {
    const filterMap = {
        'all': '',
        'live': 'المباشرة',
        'upcoming': 'القادمة',
        'finished': 'المنتهية'
    };
    
    return filterMap[filter] || '';
}
