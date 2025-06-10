// src/constants/modules.ts
export const MODULES = [
  {
    id: 'crop-classification',
    title: 'Crop Classification',
    icon: '🌱',
    description: 'Identify crops with precision using Sentinel-2 multispectral imagery and AI-powered classification algorithms.',
    image: 'https://images.unsplash.com/photo-1625246333195-78d9c38ad449?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&h=600',
    features: [
      'Sentinel-2 multispectral imagery analysis',
      'AI-powered crop identification',
      'Real-time classification updates',
      'Multi-crop type support'
    ]
  },
  {
    id: 'crop-monitoring',
    title: 'Crop Monitoring',
    icon: '📈',
    description: 'Track crop health in real-time with NDVI analysis and stress detection using advanced satellite monitoring.',
    image: 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&h=600',
    features: [
      'NDVI health monitoring',
      'Stress detection algorithms',
      'Growth stage tracking',
      'Historical trend analysis'
    ]
  },
  {
    id: 'yield-prediction',
    title: 'Yield Prediction',
    icon: '📊',
    description: 'Forecast harvest yields with machine learning models trained on historical satellite data and weather patterns.',
    image: 'https://images.unsplash.com/photo-1500595046743-cd271d694d30?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&h=600',
    features: [
      'Machine learning predictions',
      'Weather pattern integration',
      'Historical data analysis',
      'Seasonal forecasting'
    ]
  },
  {
    id: 'soil-moisture',
    title: 'Soil Moisture Analysis',
    icon: '💧',
    description: 'Monitor soil water content using Sentinel-1 radar data to optimize irrigation and water management.',
    image: 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&h=600',
    features: [
      'Sentinel-1 radar analysis',
      'Irrigation optimization',
      'Water stress alerts',
      'Moisture mapping'
    ]
  },
  {
    id: 'forest-monitoring',
    title: 'Forest Monitoring',
    icon: '🌳',
    description: 'Track forest cover changes and detect deforestation patterns using multi-temporal satellite analysis.',
    image: 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&h=600',
    features: [
      'Deforestation detection',
      'Forest cover analysis',
      'Change monitoring',
      'Conservation insights'
    ]
  },
  {
    id: 'carbon-modeling',
    title: 'Carbon Modeling',
    icon: '🍃',
    description: 'Estimate carbon sequestration and storage potential using biomass analysis and vegetation indices.',
    image: 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&h=600',
    features: [
      'Carbon sequestration estimates',
      'Biomass analysis',
      'Sustainability metrics',
      'Environmental impact'
    ]
  },
  {
    id: 'field-boundary',
    title: 'Field Boundary Detection',
    icon: '🗺️',
    description: 'Automatically map land parcels and field boundaries using advanced computer vision algorithms.',
    image: 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&h=600',
    features: [
      'Automated boundary mapping',
      'Land parcel identification',
      'GPS integration',
      'Precision agriculture support'
    ]
  },
  {
    id: 'recommendations',
    title: 'Personalized Recommendations',
    icon: '💡',
    description: 'Receive AI-powered insights and actionable recommendations tailored to your specific farming conditions.',
    image: 'https://images.unsplash.com/photo-1500937386664-56d1dfef3854?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&h=600',
    features: [
      'AI-powered insights',
      'Personalized advice',
      'Best practice recommendations',
      'Decision support tools'
    ]
  }
];

export const TESTIMONIALS = [
  {
    name: 'Amadou Diallo',
    role: 'Rice Farmer, Senegal',
    image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&h=150',
    quote: 'EcoSystem+ helped me increase my rice yield by 40% in just one season. The soil moisture alerts saved my crops during the dry spell.',
    rating: 5
  },
  {
    name: 'Dr. Fatima Mbeki',
    role: 'Agricultural Extension Officer, Kenya',
    image: 'https://images.unsplash.com/photo-1494790108755-2616b612b786?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&h=150',
    quote: 'The personalized recommendations module has revolutionized how we support smallholder farmers. Data-driven insights make all the difference.',
    rating: 5
  },
  {
    name: 'Joseph Nkomo',
    role: 'Agribusiness Manager, Ghana',
    image: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&h=150',
    quote: 'Forest monitoring capabilities helped us achieve sustainable cocoa certification. EcoSystem+ is essential for our environmental compliance.',
    rating: 5
  }
];

export const PRICING_PLANS = [
  {
    id: 'starter',
    name: 'Starter',
    icon: '🌱',
    description: 'Essential tools for small farms and new users.',
    price: 'Free',
    period: 'Forever',
    features: [
      'Basic crop monitoring',
      'NDVI health maps',
      'Email support',
    ],
    cta: 'Get Started',
    popular: false,
  },
  {
    id: 'pro',
    name: 'Pro',
    icon: '🚜',
    description: 'Advanced analytics and recommendations for growing farms.',
    price: '$19',
    period: 'per month',
    features: [
      'All Starter features',
      'Yield prediction',
      'Soil moisture analysis',
      'Personalized recommendations',
      'Priority support',
    ],
    cta: 'Start Pro',
    popular: true,
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    icon: '🌍',
    description: 'Custom solutions for agribusinesses and organizations.',
    price: 'Contact Us',
    period: '',
    features: [
      'All Pro features',
      'API access',
      'Custom integrations',
      'Dedicated account manager',
      'Onboarding & training',
    ],
    cta: 'Contact Sales',
    popular: false,
  },
];

export const FAQ_ITEMS = [
  {
    question: 'Can I try EcoSystem+ for free?',
    answer: 'Yes! The Starter plan is free forever and gives you access to basic crop monitoring and NDVI health maps.'
  },
  {
    question: 'What is included in the Pro plan?',
    answer: 'The Pro plan includes all Starter features plus yield prediction, soil moisture analysis, personalized recommendations, and priority support.'
  },
  {
    question: 'How do I upgrade to Enterprise?',
    answer: 'Contact our sales team for a custom quote and to discuss your organization’s needs. We offer API access, custom integrations, and more.'
  },
  {
    question: 'Is my data secure?',
    answer: 'Absolutely. We use industry-standard encryption and never share your data without your consent.'
  },
  {
    question: 'Can I cancel anytime?',
    answer: 'Yes, you can cancel or change your plan at any time from your account dashboard.'
  },
];
