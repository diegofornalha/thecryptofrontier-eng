import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';
import LatestNews from '../components/sections/home/LatestNews';

const meta: Meta<typeof LatestNews> = {
  title: 'Sections/Home/LatestNews',
  component: LatestNews,
  parameters: {
    layout: 'padded',
  },
  decorators: [
    (Story) => (
      <div style={{ width: '350px', height: '600px', overflow: 'auto' }}>
        <Story />
      </div>
    ),
  ],
};

export default meta;
type Story = StoryObj<typeof LatestNews>;

export const Default: Story = {};

export const InHomepage: Story = {
  decorators: [
    (Story) => (
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: '1fr 350px', 
        gap: '24px',
        backgroundColor: '#f9fafb',
        padding: '24px',
        height: '600px'
      }}>
        <div style={{ backgroundColor: '#e5e7eb', borderRadius: '8px', padding: '20px' }}>
          <p style={{ color: '#6b7280' }}>Main Content Area</p>
        </div>
        <Story />
      </div>
    ),
  ],
};