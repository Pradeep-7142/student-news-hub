import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useQuery } from "@tanstack/react-query";
import { useToast } from "@/components/ui/use-toast";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

const fetchNews = async () => {
  const response = await fetch('http://localhost:5000/api/news');
  if (!response.ok) {
    throw new Error('Failed to fetch news');
  }
  return response.json();
};

export const NewsGrid = () => {
  const { toast } = useToast();
  const { data: newsItems, isLoading, error, refetch } = useQuery({
    queryKey: ['news'],
    queryFn: fetchNews,
    meta: {
      onError: () => {
        toast({
          title: "Error",
          description: "Failed to load news. Using fallback data.",
          variant: "destructive",
        });
      }
    }
  });

  // Fallback news items if API fails
  const fallbackItems = [
    {
      title: "New Research Breakthrough in AI",
      description: "A groundbreaking discovery in artificial intelligence...",
      content: "Researchers have made significant progress...",
      image: "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=400&h=300&fit=crop",
      category: "Technology",
      url: "https://example.com/ai-breakthrough",
      source: "Tech News",
      author: "John Doe",
      publish_date: new Date().toISOString()
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
    <div className="space-y-4">
      <div className="flex justify-end">
        <Button onClick={() => refetch()} variant="outline">
          Refresh News
        </Button>
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {displayItems.map((item, index) => (
          <Card key={index} className="overflow-hidden hover:shadow-lg transition-shadow bg-[#F2FCE2]">
            <img src={item.image} alt={item.title} className="w-full h-40 object-cover" />
            <CardHeader className="p-4">
              <div className="flex gap-2 mb-2">
                <Badge variant="secondary">{item.category}</Badge>
                <Badge variant="outline">{item.source}</Badge>
              </div>
              <CardTitle className="text-lg">{item.title}</CardTitle>
            </CardHeader>
            <CardContent className="p-4 pt-0 space-y-3">
              <p className="text-sm text-muted-foreground line-clamp-2">
                {item.description}
              </p>
              <div className="text-xs text-muted-foreground">
                {item.author && <p>By: {item.author}</p>}
                <p>Published: {new Date(item.publish_date).toLocaleDateString()}</p>
              </div>
              <div className="space-y-2">
                <p className="text-sm line-clamp-3">{item.content}</p>
                <Button 
                  variant="link" 
                  className="p-0 h-auto text-primary"
                  onClick={() => window.open(item.url, '_blank')}
                >
                  Read full article →
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};
