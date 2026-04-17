'use client';

import { useState } from 'react';

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="fixed top-0 w-full z-50 bg-black/80 backdrop-blur-md border-b border-gray-800">
      <nav className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-pink-500 rounded-lg flex items-center justify-center font-bold text-white">
            G
          </div>
          <span className="text-xl font-bold">GenOpsLab</span>
        </div>

        {/* Desktop Navigation */}
        <div className="hidden md:flex items-center gap-8">
          <a href="#features" className="text-gray-400 hover:text-white transition-colors">
            Features
          </a>
          <a href="#howitworks" className="text-gray-400 hover:text-white transition-colors">
            How it works
          </a>
          <a href="#why" className="text-gray-400 hover:text-white transition-colors">
            Why us
          </a>
          <button className="text-indigo-400 hover:text-indigo-300 font-semibold">
            Sign in
          </button>
          <button className="gradient-button text-sm py-2 px-4">
            Get started
          </button>
        </div>

        {/* Mobile menu button */}
        <button
          className="md:hidden text-white"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="absolute top-16 left-0 right-0 bg-black/95 border-b border-gray-800 md:hidden">
            <div className="px-4 py-4 flex flex-col gap-4">
              <a href="#features" className="text-gray-400 hover:text-white transition-colors">
                Features
              </a>
              <a href="#howitworks" className="text-gray-400 hover:text-white transition-colors">
                How it works
              </a>
              <a href="#why" className="text-gray-400 hover:text-white transition-colors">
                Why us
              </a>
              <button className="text-indigo-400 hover:text-indigo-300 font-semibold">
                Sign in
              </button>
              <button className="gradient-button text-sm py-2 px-4">
                Get started
              </button>
            </div>
          </div>
        )}
      </nav>
    </header>
  );
}
