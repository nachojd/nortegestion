import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  assetPrefix: process.env.NODE_ENV === 'production' ? undefined : '',
<<<<<<< HEAD
  output: 'standalone'
=======
  experimental: {
    allowedOrigins: ['*']
  }
>>>>>>> main
};

export default nextConfig;
