import './globals.css';
import type { Metadata } from 'next';
export const metadata: Metadata = { title: 'Imperial Bank | Demo Banking', description: 'Imperial Bank simulated digital banking experience' };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body>{children}</body></html>; }
