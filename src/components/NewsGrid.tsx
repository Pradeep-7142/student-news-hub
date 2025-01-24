import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const newsItems = [
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
];

export const NewsGrid = () => {
  return (
    <div className="news-grid">
      {newsItems.map((item, index) => (
        <Card key={index} className="overflow-hidden hover:shadow-lg transition-shadow">
          <img src={item.image} alt={item.title} className="w-full h-48 object-cover" />
          <CardHeader>
            <div className="text-sm text-primary font-medium">{item.category}</div>
            <CardTitle className="text-xl">{item.title}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">
              Click to read more about this exciting news story...
            </p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};