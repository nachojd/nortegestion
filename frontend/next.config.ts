import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  assetPrefix: process.env.NODE_ENV === 'production' ? undefined : '',
  experimental: {
    allowedOrigins: ['*']
  },
  output: 'standalone'
};

export default nextConfig;
