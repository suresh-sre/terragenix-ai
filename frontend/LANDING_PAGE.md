# GenOpsLab Landing Page

A modern, high-conversion SaaS landing page for GenOpsLab—an AI-powered Cloud & DevOps platform.

## 🎨 Features

- **Modern SaaS Design**: Minimal UI with clean spacing inspired by ZorvaPulse
- **Dark Theme with Gradients**: Professional gradient buttons and cards
- **Smooth Animations**: Fade-in and slide-in effects for engaging UX
- **Fully Responsive**: Mobile-first design that works on all devices
- **Component-Based**: Reusable React components for easy maintenance
- **Tailwind CSS**: Utility-first styling with custom animations
- **Performance Optimized**: Next.js with static generation for fast load times

## 📁 Project Structure

```
genopslab/
├── app/
│   ├── components/
│   │   ├── Header.tsx         # Navigation header with mobile menu
│   │   ├── Hero.tsx           # Hero section with CTA buttons
│   │   ├── Features.tsx       # 3-card feature showcase
│   │   ├── HowItWorks.tsx     # 4-step process visualization
│   │   ├── TargetUsers.tsx    # Target audience cards
│   │   ├── WhyUs.tsx          # Why choose GenOpsLab section
│   │   ├── FinalCTA.tsx       # Final call-to-action section
│   │   └── Footer.tsx         # Footer with links and social
│   ├── globals.css            # Global styles and animations
│   ├── layout.tsx             # Root layout with metadata
│   └── page.tsx               # Home page composition
├── public/                     # Static assets
├── package.json               # Dependencies
├── tailwind.config.ts         # Tailwind configuration
└── tsconfig.json              # TypeScript configuration
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

```bash
# Navigate to the genopslab directory
cd genopslab

# Install dependencies
npm install

# Start the development server
npm run dev
```

Navigate to [http://localhost:3000](http://localhost:3000) to see your landing page.

## 📦 Build & Deploy

### Build for production:
```bash
npm run build
npm start
```

### Deploy to Vercel:
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

Vercel provides automatic deployments on every git push. The site is optimized for edge deployment with zero-config setup.

## 🎯 Sections Overview

### 1. **Hero Section**
- Bold headline with gradient text
- Subheading describing value proposition
- Dual CTA buttons (Start Building & View Demo)
- Trust indicator with user count

### 2. **Features** (3 cards)
- Generate Infrastructure (Terraform AI)
- Cost Optimization (FinOps)
- Real Projects (Portfolio Builder)

### 3. **How It Works**
- 4-step process with connected visualization
- Numbered steps with descriptions
- Gradient accents and hover effects

### 4. **Target Users**
- Students (Learn & Build)
- Professionals (Accelerate Career)
- Startups (Scale Fast)

### 5. **Why Us**
- AI-Powered DevOps
- Real-World Projects
- Cost-Aware Design
- Career-Focused Platform

### 6. **Final CTA**
- Strong headline
- Dual action buttons
- Trust indicators (companies using GenOpsLab)
- No credit card required message

## 🎨 Design System

### Colors
- **Primary**: Indigo (`#6366f1`)
- **Accent**: Pink (`#ec4899`)
- **Background**: Black (`#0a0a0a`)
- **Text**: Light Gray (`#f5f5f5`)

### Typography
- Large, bold headlines (text-6xl to text-7xl)
- Medium body copy (text-lg)
- Consistent spacing with Tailwind's spacing scale

### Components
- **Gradient Buttons**: `.gradient-button` class
- **Cards**: `.card` class with hover effects
- **Animations**: Fade-in, fade-in-up, slide-in effects

## 🔧 Customization

### Update Product Information
Edit the text content in each component file. Most copy is in JSX.

### Change Colors
Update the CSS variables in `globals.css`:
```css
:root {
  --primary: #6366f1;    /* Change primary color */
  --accent: #ec4899;     /* Change accent color */
}
```

### Add New Sections
1. Create a new component in `app/components/`
2. Import it in `app/page.tsx`
3. Add it to the component composition

### Update Links
Replace `#` with actual URLs in:
- `Header.tsx` - Navigation links
- `Footer.tsx` - Footer links
- `FinalCTA.tsx` - CTA button links

## 📱 Responsive Breakpoints

The design uses Tailwind's responsive prefixes:
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px

All sections are optimized for mobile-first design.

## ⚡ Performance

- **Static Generation**: All pages prerendered at build time
- **Image Optimization**: Next.js Image component ready
- **Code Splitting**: Automatic code splitting per route
- **CSS**: Tailwind CSS with purging of unused styles

## 📝 SEO

Metadata includes:
- Descriptive title and description
- Open Graph tags for social sharing
- Keywords for search indexing
- Robots meta tag for crawling

## 🛠️ Tech Stack

- **Framework**: [Next.js 16.2.4](https://nextjs.org)
- **UI Library**: [React 19.2.4](https://react.dev)
- **Styling**: [Tailwind CSS 4](https://tailwindcss.com)
- **Language**: [TypeScript 5](https://www.typescriptlang.org)
- **Runtime**: Node.js

## 📖 Local Development

### Watch mode
```bash
npm run dev
```

### Type checking
```bash
npm run lint
```

### Build check
```bash
npm run build
```

## 🌐 Environment Setup

No additional environment variables required. The landing page is fully static and works out of the box.

For analytics, API integrations, or forms, add environment variables to `.env.local`:
```
NEXT_PUBLIC_API_URL=your_api_url
```

## 📄 License

This landing page template is ready for commercial use. Customize it with your brand, content, and deployment.

## 🤝 Support

For issues or questions:
1. Check the [Next.js documentation](https://nextjs.org/docs)
2. Review [Tailwind CSS docs](https://tailwindcss.com/docs)
3. Refer to component code comments

---

Built with ❤️ for GenOpsLab | Ready to deploy on Vercel
