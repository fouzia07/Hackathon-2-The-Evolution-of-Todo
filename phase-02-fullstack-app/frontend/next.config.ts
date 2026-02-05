import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: false,
  },
  experimental: {
    turbo: {
      resolveAlias: {
        '@/*': ['./src/*', './*'],
      },
    },
  },
};

export default nextConfig;
