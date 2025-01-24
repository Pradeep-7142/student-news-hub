import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const trendingNews = [
  {
    title: "Breaking: New Campus Library Opening",
    category: "Campus",
  },
  {
    title: "Student Achievement Awards 2024",
    category: "Events",
  },
  {
    title: "Important: Course Registration Deadlines",
    category: "Academic",
  },
  {
    title: "New Research Grant Opportunities",
    category: "Research",
  },
];

export const TrendingNews = () => {
  return (
    <div className="w-full mb-8">
      <h2 className="text-2xl font-semibold mb-4">Trending News</h2>
      <Carousel
        opts={{
          align: "start",
          loop: true,
        }}
        className="w-full"
      >
        <CarouselContent>
          {trendingNews.map((news, index) => (
            <CarouselItem key={index} className="md:basis-1/3 lg:basis-1/4">
              <Card className="h-32">
                <CardHeader className="p-4">
                  <div className="text-sm text-primary font-medium">{news.category}</div>
                  <CardTitle className="text-base">{news.title}</CardTitle>
                </CardHeader>
              </Card>
            </CarouselItem>
          ))}
        </CarouselContent>
        <CarouselPrevious />
        <CarouselNext />
      </Carousel>
    </div>
  );
};