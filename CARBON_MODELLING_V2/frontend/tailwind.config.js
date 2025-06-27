/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx,vue}",
    "./**/*.{html,js,vue}"
  ],
  theme: {
    extend: {
      // Agricultural & Earth Tone Color Palette
      colors: {
        // Primary Agricultural Greens
        forest: {
          50: '#f0fdf4',   // Lightest green - backgrounds
          100: '#dcfce7',  // Light green - subtle highlights
          200: '#bbf7d0',  // Soft green - hover states
          300: '#86efac',  // Medium light - accents
          400: '#4ade80',  // Medium - secondary buttons
          500: '#22c55e',  // Primary brand green
          600: '#16a34a',  // Primary hover
          700: '#15803d',  // Primary active
          800: '#166534',  // Dark green - text
          900: '#14532d',  // Darkest - headings
          950: '#052e16'   // Extra dark - contrast
        },
        
        // Earth Tones
        earth: {
          50: '#fefcf3',   // Cream white
          100: '#fef7e4',  // Light cream
          200: '#fdeec4',  // Warm beige
          300: '#fbd894',  // Light earth
          400: '#f7bc5c',  // Medium earth
          500: '#f59e0b',  // Primary earth
          600: '#d97706',  // Earth hover
          700: '#b45309',  // Earth active
          800: '#92400e',  // Dark earth
          900: '#78350f',  // Darkest earth
          950: '#451a03'   // Extra dark earth
        },
        
        // Clay/Soil Tones
        clay: {
          50: '#faf7f4',   // Light clay
          100: '#f4ede6',  // Soft clay
          200: '#e6d5c7',  // Medium clay
          300: '#d4b5a0',  // Clay accent
          400: '#c19579',  // Medium clay
          500: '#a67c5a',  // Primary clay
          600: '#8b6646',  // Clay hover
          700: '#7a5a41',  // Clay active
          800: '#644b36',  // Dark clay
          900: '#533e2e',  // Darkest clay
          950: '#2d1f19'   // Extra dark clay
        },
        
        // Agricultural Sky
        sky: {
          50: '#f0f9ff',   // Lightest sky
          100: '#e0f2fe',  // Light sky
          200: '#bae6fd',  // Soft sky
          300: '#7dd3fc',  // Medium sky
          400: '#38bdf8',  // Sky accent
          500: '#0ea5e9',  // Primary sky
          600: '#0284c7',  // Sky hover
          700: '#0369a1',  // Sky active
          800: '#075985',  // Dark sky
          900: '#0c4a6e',  // Darkest sky
          950: '#082f49'   // Extra dark sky
        },
        
        // Semantic Colors
        success: {
          50: '#f0fdf4',
          500: '#22c55e',
          600: '#16a34a',
          700: '#15803d'
        },
        warning: {
          50: '#fffbeb',
          500: '#f59e0b',
          600: '#d97706',
          700: '#b45309'
        },
        error: {
          50: '#fef2f2',
          500: '#ef4444',
          600: '#dc2626',
          700: '#b91c1c'
        },
        info: {
          50: '#f0f9ff',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1'
        },
        
        // Neutral Grays
        neutral: {
          50: '#fafaf9',   // Almost white
          100: '#f5f5f4',  // Light gray
          200: '#e7e5e4',  // Soft gray
          300: '#d6d3d1',  // Medium light
          400: '#a8a29e',  // Medium gray
          500: '#78716c',  // Primary gray
          600: '#57534e',  // Gray hover
          700: '#44403c',  // Gray active
          800: '#292524',  // Dark gray
          900: '#1c1917',  // Darkest gray
          950: '#0c0a09'   // Extra dark
        }
      },
      
      // Typography Scale
      fontFamily: {
        'sans': ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        'serif': ['Crimson Text', 'Georgia', 'serif'],
        'mono': ['JetBrains Mono', 'Fira Code', 'monospace']
      },
      
      fontSize: {
        'xs': ['0.75rem', { lineHeight: '1rem' }],         // 12px
        'sm': ['0.875rem', { lineHeight: '1.25rem' }],     // 14px
        'base': ['1rem', { lineHeight: '1.5rem' }],        // 16px
        'lg': ['1.125rem', { lineHeight: '1.75rem' }],     // 18px
        'xl': ['1.25rem', { lineHeight: '1.75rem' }],      // 20px
        '2xl': ['1.5rem', { lineHeight: '2rem' }],         // 24px
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],    // 30px
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],      // 36px
        '5xl': ['3rem', { lineHeight: '1' }],              // 48px
        '6xl': ['3.75rem', { lineHeight: '1' }],           // 60px
        '7xl': ['4.5rem', { lineHeight: '1' }],            // 72px
        '8xl': ['6rem', { lineHeight: '1' }],              // 96px
        '9xl': ['8rem', { lineHeight: '1' }]               // 128px
      },
      
      // Spacing Scale (8px base)
      spacing: {
        '0.5': '0.125rem',   // 2px
        '1': '0.25rem',      // 4px
        '1.5': '0.375rem',   // 6px
        '2': '0.5rem',       // 8px
        '2.5': '0.625rem',   // 10px
        '3': '0.75rem',      // 12px
        '3.5': '0.875rem',   // 14px
        '4': '1rem',         // 16px
        '5': '1.25rem',      // 20px
        '6': '1.5rem',       // 24px
        '7': '1.75rem',      // 28px
        '8': '2rem',         // 32px
        '9': '2.25rem',      // 36px
        '10': '2.5rem',      // 40px
        '11': '2.75rem',     // 44px
        '12': '3rem',        // 48px
        '14': '3.5rem',      // 56px
        '16': '4rem',        // 64px
        '20': '5rem',        // 80px
        '24': '6rem',        // 96px
        '28': '7rem',        // 112px
        '32': '8rem',        // 128px
        '36': '9rem',        // 144px
        '40': '10rem',       // 160px
        '44': '11rem',       // 176px
        '48': '12rem',       // 192px
        '52': '13rem',       // 208px
        '56': '14rem',       // 224px
        '60': '15rem',       // 240px
        '64': '16rem',       // 256px
        '72': '18rem',       // 288px
        '80': '20rem',       // 320px
        '96': '24rem'        // 384px
      },
      
      // Border Radius
      borderRadius: {
        'none': '0',
        'sm': '0.125rem',     // 2px
        'DEFAULT': '0.25rem', // 4px
        'md': '0.375rem',     // 6px
        'lg': '0.5rem',       // 8px
        'xl': '0.75rem',      // 12px
        '2xl': '1rem',        // 16px
        '3xl': '1.5rem',      // 24px
        '4xl': '2rem',        // 32px
        'full': '9999px'
      },
      
      // Box Shadows
      boxShadow: {
        'xs': '0 1px 2px 0 rgb(0 0 0 / 0.05)',
        'sm': '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
        'DEFAULT': '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
        'md': '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
        'lg': '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
        'xl': '0 25px 50px -12px rgb(0 0 0 / 0.25)',
        '2xl': '0 50px 100px -20px rgb(0 0 0 / 0.25)',
        'inner': 'inset 0 2px 4px 0 rgb(0 0 0 / 0.05)',
        
        // Custom agricultural shadows
        'glow-green': '0 0 20px rgba(34, 197, 94, 0.3)',
        'glow-green-lg': '0 0 40px rgba(34, 197, 94, 0.4)',
        'glow-earth': '0 0 20px rgba(245, 158, 11, 0.3)',
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
        'clay': '0 4px 14px 0 rgba(166, 124, 90, 0.39)'
      },
      
      // Animations
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'fade-out': 'fadeOut 0.5s ease-in-out',
        'slide-up': 'slideUp 0.5s ease-out',
        'slide-down': 'slideDown 0.5s ease-out',
        'slide-in-left': 'slideInLeft 0.5s ease-out',
        'slide-in-right': 'slideInRight 0.5s ease-out',
        'scale-in': 'scaleIn 0.3s ease-out',
        'scale-out': 'scaleOut 0.3s ease-in',
        'float': 'float 6s ease-in-out infinite',
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce-slow': 'bounce 3s infinite',
        'wiggle': 'wiggle 1s ease-in-out infinite',
        'gradient': 'gradient 15s ease infinite',
        'shimmer': 'shimmer 2s linear infinite'
      },
      
      // Keyframes
      keyframes: {
        fadeIn: {
          'from': { opacity: '0' },
          'to': { opacity: '1' }
        },
        fadeOut: {
          'from': { opacity: '1' },
          'to': { opacity: '0' }
        },
        slideUp: {
          'from': { transform: 'translateY(100%)', opacity: '0' },
          'to': { transform: 'translateY(0)', opacity: '1' }
        },
        slideDown: {
          'from': { transform: 'translateY(-100%)', opacity: '0' },
          'to': { transform: 'translateY(0)', opacity: '1' }
        },
        slideInLeft: {
          'from': { transform: 'translateX(-100%)', opacity: '0' },
          'to': { transform: 'translateX(0)', opacity: '1' }
        },
        slideInRight: {
          'from': { transform: 'translateX(100%)', opacity: '0' },
          'to': { transform: 'translateX(0)', opacity: '1' }
        },
        scaleIn: {
          'from': { transform: 'scale(0.95)', opacity: '0' },
          'to': { transform: 'scale(1)', opacity: '1' }
        },
        scaleOut: {
          'from': { transform: 'scale(1)', opacity: '1' },
          'to': { transform: 'scale(0.95)', opacity: '0' }
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px) rotate(0deg)' },
          '25%': { transform: 'translateY(-20px) rotate(1deg)' },
          '50%': { transform: 'translateY(-10px) rotate(-1deg)' },
          '75%': { transform: 'translateY(-15px) rotate(0.5deg)' }
        },
        wiggle: {
          '0%, 100%': { transform: 'rotate(-3deg)' },
          '50%': { transform: 'rotate(3deg)' }
        },
        gradient: {
          '0%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
          '100%': { backgroundPosition: '0% 50%' }
        },
        shimmer: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' }
        }
      },
      
      // Background Images
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'agricultural-mesh': `
          radial-gradient(at 40% 20%, hsla(142, 100%, 30%, 0.3) 0px, transparent 50%),
          radial-gradient(at 80% 0%, hsla(142, 100%, 40%, 0.2) 0px, transparent 50%),
          radial-gradient(at 0% 50%, hsla(142, 100%, 35%, 0.1) 0px, transparent 50%),
          radial-gradient(at 80% 50%, hsla(142, 100%, 30%, 0.2) 0px, transparent 50%)
        `,
        'earth-gradient': 'linear-gradient(135deg, #f59e0b 0%, #d97706 50%, #b45309 100%)',
        'forest-gradient': 'linear-gradient(135deg, #22c55e 0%, #16a34a 50%, #15803d 100%)',
        'clay-gradient': 'linear-gradient(135deg, #a67c5a 0%, #8b6646 50%, #7a5a41 100%)'
      },
      
      // Backdrop Blur
      backdropBlur: {
        'xs': '2px',
        'sm': '4px',
        'DEFAULT': '8px',
        'md': '12px',
        'lg': '16px',
        'xl': '24px',
        '2xl': '40px',
        '3xl': '64px'
      }
    }
  },
  plugins: [
    // Add any additional plugins here
  ]
}
