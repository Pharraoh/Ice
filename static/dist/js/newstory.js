document.addEventListener('DOMContentLoaded', () => {

    // --- Dummy Data for Stories ---
    const storiesData = {
        "user123": {
            username: "alex_codes",
            pfp: "https://i.pravatar.cc/150?u=alex_codes",
            stories: [
                { type: 'image', url: 'https://images.unsplash.com/photo-1554310624-0515150a316c?q=80&w=1887', duration: 5000, caption: "Exploring the mountains! 🏔️" },
                { type: 'text', background: 'linear-gradient(45deg, #ff8177, #ff867a, #f99185, #cf556c, #b12a5b)', duration: 4000, caption: "What a beautiful day." },
                { type: 'image', url: 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?q=80&w=1980', duration: 6000, caption: "City nights ✨" }
            ]
        },
        "user456": {
            username: "sara.designs",
            pfp: "https://i.pravatar.cc/150?u=sara.designs",
            stories: [
                { type: 'image', url: 'https://images.unsplash.com/photo-1551963831-b3b1ca40c98e?q=80&w=2070', duration: 5000, caption: "Foodie adventures!" },
                { type: 'image', url: 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?q=80&w=2070', duration: 5000, caption: "Dream home goals." },
            ]
        }
    };

    // --- DOM Elements ---
    const storyViewer = document.getElementById('story-viewer');
    const storyPfp = document.getElementById('story-pfp');
    const storyUsername = document.getElementById('story-username');
    const closeBtn = document.querySelector('.close-story-btn');
    const progressBarsContainer = document.querySelector('.progress-bars');
    const mediaContainer = document.getElementById('story-media');
    const captionContainer = document.getElementById('story-caption');
    const navPrev = document.querySelector('.nav-zone.prev');
    const navNext = document.querySelector('.nav-zone.next');

    // --- State Variables ---
    let currentUserStories = [];
    let currentStoryIndex = 0;
    let storyTimer;

    // --- Main Functions ---
    const openStoryViewer = (userId) => {
        const userData = storiesData[userId];
        if (!userData || userData.stories.length === 0) return;

        currentUserStories = userData;
        storyUsername.textContent = currentUserStories.username;
        storyPfp.src = currentUserStories.pfp;

        buildProgressBars();
        showStory(0); // Start from the first story

        storyViewer.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    };

    const closeStoryViewer = () => {
        storyViewer.classList.add('hidden');
        document.body.style.overflow = 'auto';
        clearTimeout(storyTimer);
        progressBarsContainer.innerHTML = '';
        mediaContainer.innerHTML = '';
        captionContainer.textContent = '';
    };

    const buildProgressBars = () => {
        progressBarsContainer.innerHTML = '';
        currentUserStories.stories.forEach(() => {
            const bar = document.createElement('div');
            bar.classList.add('progress-bar');
            bar.innerHTML = '<div class="filler"></div>';
            progressBarsContainer.appendChild(bar);
        });
    };

    const showStory = (index) => {
        if (index < 0) { index = 0; } // Don't go before the first
        if (index >= currentUserStories.stories.length) {
            closeStoryViewer();
            return;
        }
        currentStoryIndex = index;
        const story = currentUserStories.stories[currentStoryIndex];

        mediaContainer.innerHTML = '';
        captionContainer.textContent = '';

        Array.from(progressBarsContainer.children).forEach((bar, i) => {
            bar.classList.remove('active');
            bar.firstElementChild.style.animation = 'none';
            if (i < currentStoryIndex) {
                bar.firstElementChild.style.width = '100%';
            } else {
                bar.firstElementChild.style.width = '0%';
            }
        });

        setTimeout(() => {
            const activeBar = progressBarsContainer.children[currentStoryIndex];
            if(activeBar) {
                activeBar.classList.add('active');
                activeBar.firstElementChild.style.animationDuration = `${story.duration / 1000}s`;
            }

            if (story.type === 'image') {
                mediaContainer.style.background = '#1a1a1a';
                mediaContainer.innerHTML = `<img src="${story.url}" alt="Story media">`;
            } else if (story.type === 'text') {
                mediaContainer.style.background = story.background;
            }
            captionContainer.textContent = story.caption;
        }, 50);

        clearTimeout(storyTimer);
        storyTimer = setTimeout(nextStory, story.duration);
    };

    const nextStory = () => showStory(currentStoryIndex + 1);
    const prevStory = () => showStory(currentStoryIndex - 1);

    const pauseStory = () => {
        const activeFiller = document.querySelector('.progress-bar.active > .filler');
        if (activeFiller) activeFiller.style.animationPlayState = 'paused';
        clearTimeout(storyTimer);
    };

    const resumeStory = () => {
        const activeFiller = document.querySelector('.progress-bar.active > .filler');
        if (activeFiller) {
             activeFiller.style.animationPlayState = 'running';
             const computedStyle = getComputedStyle(activeFiller);
             const animationDuration = parseFloat(computedStyle.animationDuration) * 1000;
             const width = parseFloat(computedStyle.width) / parseFloat(getComputedStyle(activeFiller.parentElement).width);
             const remainingTime = animationDuration * (1 - width);
             clearTimeout(storyTimer);
             storyTimer = setTimeout(nextStory, remainingTime);
        }
    };

    // --- Event Listeners ---
    closeBtn.addEventListener('click', closeStoryViewer);
    navNext.addEventListener('click', nextStory);
    navPrev.addEventListener('click', prevStory);
    storyViewer.addEventListener('mousedown', pauseStory);
    storyViewer.addEventListener('mouseup', resumeStory);
    storyViewer.addEventListener('touchstart', pauseStory, { passive: true });
    storyViewer.addEventListener('touchend', resumeStory);

    document.querySelectorAll('.story-trigger-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            openStoryViewer(btn.dataset.userid);
        });
    });
});
