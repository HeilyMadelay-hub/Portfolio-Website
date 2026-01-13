// 🚨 EmergencyMode.js - Fallback responses when backend is unavailable
// This module allows the chat to keep working with predefined responses

class EmergencyMode {
    constructor() {
        this.isActive = false;
        this.activationReason = '';

        // 📚 Predefined responses by category
        this.responses = {
            // Greetings
            greeting: [
                "Hello! 👋 I'm MadGPT, Heily's virtual assistant. I'm currently in offline mode, but I can give you basic information.",
                "Welcome! 🌟 I'm running in limited mode, but I can still help you with general information about Heily.",
            ],

            // About Heily
            about: [
                "Heily is a **Full Stack & MultiCloud Developer** passionate about building scalable AI solutions. She has experience in Python, JavaScript, React, FastAPI, and cloud services like AWS, GCP, and Azure.",
                "Heily specializes in modern web development, cloud architectures, and artificial intelligence applications. She loves creating innovative projects that combine these technologies.",
            ],

            // Skills
            skills: [
                "**Heily's main technologies:**\n\n• **Frontend:** React, TypeScript, Vite, TailwindCSS\n• **Backend:** Python, FastAPI, Node.js\n• **Cloud:** AWS, Google Cloud, Azure\n• **AI/ML:** LangChain, ChromaDB, Gemini API\n• **DevOps:** Docker, Kubernetes, CI/CD",
                "Heily masters the full stack: from modern interfaces with React to robust backends with FastAPI, including cloud infrastructure and AI solutions.",
            ],

            // Projects
            projects: [
                "**Heily's featured projects:**\n\n🤖 **MadGPT** - This AI chatbot you're using right now\n☁️ **Cloud Infrastructure** - Scalable architectures on AWS/GCP\n📊 **Analytics Dashboards** - Real-time data visualization",
                "Heily has worked on AI chatbot projects, RAG systems, full-stack web applications, and enterprise cloud architectures.",
            ],

            // Contact
            contact: [
                "**Ways to contact Heily:**\n\n📧 Email: [available on portfolio]\n💼 LinkedIn: [professional profile]\n🐙 GitHub: [public repositories]\n\nFeel free to reach out!",
                "You can find Heily's contact information in the contact section of the portfolio. She's always open to new opportunities!",
            ],

            // Experience
            experience: [
                "Heily has experience working with modern web development and cloud technologies. She has participated in projects involving microservices architectures, AI systems, and scalable applications.",
                "Her experience spans from frontend development with React to backend with Python/FastAPI, including deployments on multiple cloud platforms.",
            ],

            // Education/Certifications
            education: [
                "Heily has certifications in cloud computing and is constantly learning new technologies. You can see more details on her LinkedIn profile.",
            ],

            // Default response
            default: [
                "Thanks for your question! 🤔 I'm in offline mode right now, so my response capacity is limited. When the backend is available, I'll be able to give you much more detailed and personalized answers.\n\n**Meanwhile, I suggest:**\n• Explore the portfolio sections\n• Check out Heily's projects\n• Try again in a few minutes",
                "Hmm, that's a good question, but I need the backend to give you a complete answer. 🔧 I'm running in emergency mode.\n\nCan I help you with something more basic like information about Heily, her skills, or projects?",
            ],

            // System error
            systemError: [
                "⚠️ **Offline Mode Active**\n\nThe server is not available at this time. I'm running with limited responses.\n\nHow can I help you in the meantime?",
            ],
        };

        // 🔍 Keywords to detect intent
        this.keywords = {
            greeting: ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'greetings', 'what\'s up', 'howdy'],
            about: ['who is', 'about heily', 'about', 'tell me', 'introduction', 'description', 'who are you'],
            skills: ['skills', 'technologies', 'technology', 'know how', 'knowledge', 'languages', 'frameworks', 'tools', 'stack'],
            projects: ['projects', 'portfolio', 'work', 'created', 'developed', 'applications', 'built'],
            contact: ['contact', 'email', 'linkedin', 'github', 'social', 'reach', 'write', 'talk'],
            experience: ['experience', 'work', 'jobs', 'career', 'trajectory', 'background'],
            education: ['studies', 'education', 'certifications', 'courses', 'training', 'university', 'degree'],
        };
    }

    /**
     * 🔥 Activate emergency mode
     */
    activate(reason = 'Backend not available') {
        this.isActive = true;
        this.activationReason = reason;
        console.warn('🚨 Emergency mode ACTIVATED:', reason);
    }

    /**
     * ✅ Deactivate emergency mode
     */
    deactivate() {
        this.isActive = false;
        this.activationReason = '';
        console.log('✅ Emergency mode DEACTIVATED');
    }

    /**
     * 🎯 Detect message intent
     */
    detectIntent(message) {
        const lowerMessage = message.toLowerCase().trim();

        for (const [intent, keywords] of Object.entries(this.keywords)) {
            for (const keyword of keywords) {
                if (lowerMessage.includes(keyword)) {
                    return intent;
                }
            }
        }

        return 'default';
    }

    /**
     * 🎲 Get random response from category
     */
    getRandomResponse(category) {
        const responses = this.responses[category] || this.responses.default;
        const randomIndex = Math.floor(Math.random() * responses.length);
        return responses[randomIndex];
    }

    /**
     * 📤 Generate emergency response
     */
    generateResponse(message) {
        const intent = this.detectIntent(message);
        const response = this.getRandomResponse(intent);

        return {
            response: response,
            metadata: {
                source: 'emergency_mode',
                intent: intent,
                isOffline: true,
                reason: this.activationReason,
                timestamp: Date.now(),
            },
            error: null,
            isEmergency: true,
        };
    }

    /**
     * 🏥 Get initial offline mode message
     */
    getOfflineGreeting() {
        return this.getRandomResponse('systemError');
    }
}

// Export unique instance (singleton)
const emergencyMode = new EmergencyMode();
export default emergencyMode;