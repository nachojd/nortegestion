import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  assetPrefix: process.env.NODE_ENV === 'production' ? undefined : '',
  output: 'standalone'
};

export default nextConfig;
