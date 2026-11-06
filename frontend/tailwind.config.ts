import type { Config } from 'tailwindcss';
const config: Config = { content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'], theme: { extend: { colors: { imperial: { navy: '#101D35', gold: '#C8A85B', ink: '#182235', muted: '#718096' } }, boxShadow: { soft: '0 12px 35px rgba(16,29,53,.07)' } } }, plugins: [] };
export default config;
