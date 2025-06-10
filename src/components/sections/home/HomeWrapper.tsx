'use client';

import dynamic from 'next/dynamic';

const Home = dynamic(() => import('./Home'), {
  ssr: false,
  loading: () => (
    <div className="bg-white">
      <div className="max-w-7xl mx-auto px-4 py-8 pb-16">
        <div className="flex flex-col lg:flex-row">
          <div className="w-full lg:w-1/4 lg:pr-6">
            <div className="h-96 bg-gray-100 animate-pulse rounded-lg"></div>
          </div>
          <div className="w-full lg:w-1/2 lg:px-6">
            <div className="h-96 bg-gray-100 animate-pulse rounded-lg"></div>
          </div>
          <div className="w-full lg:w-1/4 lg:pl-6">
            <div className="h-96 bg-gray-100 animate-pulse rounded-lg"></div>
          </div>
        </div>
      </div>
    </div>
  ),
});

export default Home;