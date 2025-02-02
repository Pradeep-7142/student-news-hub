import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useQuery } from "@tanstack/react-query";
import { useToast } from "@/components/ui/use-toast";

const fetchNews = async () => {
  const response = await fetch('http://localhost:5000/api/news');
  if (!response.ok) {
    throw new Error('Failed to fetch news');
  }
  return response.json();
};

export const NewsGrid = () => {
  const { toast } = useToast();
  const { data: newsItems, isLoading, error } = useQuery({
    queryKey: ['news'],
    queryFn: fetchNews,
    onError: (error) => {
      toast({
        title: "Error",
        description: "Failed to load news. Using fallback data.",
        variant: "destructive",
      });
      console.error('Error fetching news:', error);
    },
  });

  // Fallback news items if API fails
  const fallbackItems = [
    {
      title: "New Research Breakthrough in AI",
      image: "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=400&h=300&fit=crop",
      category: "Technology",
    },
    {
      title: "Campus Life Post-Pandemic",
      image: "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=400&h=300&fit=crop",
      category: "Campus",
    },
    {
      title: "Future of Remote Learning",
      image: "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=400&h=300&fit=crop",
      category: "Education",
    },
    {
      title: "Student Success Stories",
      image: "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=400&h=300&fit=crop",
      category: "Success",
    },
    {
      title: "Sports Team Achievements",
      image: "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=400&h=300&fit=crop",
      category: "Sports",
    },
    {
      title: "Arts Festival Coming Soon",
      image: "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?w=400&h=300&fit=crop",
      category: "Arts",
    },
  ];

  const displayItems = newsItems || fallbackItems;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
      {displayItems.map((item, index) => (
        <Card key={index} className="overflow-hidden hover:shadow-lg transition-shadow bg-[#F2FCE2]">
          <img src={item.image} alt={item.title} className="w-full h-40 object-cover" />
          <CardHeader className="p-4">
            <div className="text-sm text-primary font-medium">{item.category}</div>
            <CardTitle className="text-lg">{item.title}</CardTitle>
          </CardHeader>
          <CardContent className="p-4 pt-0">
            <p className="text-sm text-muted-foreground">
              Click to read more about this exciting news story...
            </p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};
