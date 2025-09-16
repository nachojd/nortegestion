import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Allow login page and static assets
  if (pathname.startsWith('/login') ||
      pathname.startsWith('/_next') ||
      pathname.startsWith('/favicon') ||
      pathname.startsWith('/api')) {
    return NextResponse.next();
  }

  // Check for authentication tokens on protected routes
  const tokens = request.cookies.get('nortegestion_tokens');
  const authHeader = request.headers.get('authorization');

  // If no tokens in cookies and no auth header, redirect to login
  if (!tokens && !authHeader) {
    // For the root path, redirect to login if not authenticated
    if (pathname === '/' || pathname.startsWith('/products') || pathname.startsWith('/quotes')) {
      const loginUrl = new URL('/login', request.url);
      return NextResponse.redirect(loginUrl);
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};