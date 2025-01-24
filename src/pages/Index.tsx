import { Navbar } from "@/components/Navbar";
import { FieldTabs } from "@/components/FieldTabs";
import { NewsGrid } from "@/components/NewsGrid";
import { TrendingNews } from "@/components/TrendingNews";
import { Footer } from "@/components/Footer";

const Index = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <div 
        className="fixed inset-0 -z-10 opacity-10"
        style={{
          backgroundImage: "url('https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?auto=format&fit=crop&w=2000')",
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      />
      
      <Navbar />
      
      <main className="flex-1 container mx-auto px-4 pt-24">
        <h1 className="text-4xl font-bold text-center mb-8">
          Student News Hub
        </h1>
        
        <FieldTabs />
        
        <section className="mt-12">
          <TrendingNews />
          
          <h2 className="text-2xl font-semibold mb-8">Latest News</h2>
          <NewsGrid />
        </section>
      </main>
      
      <Footer />
    </div>
  );
};

export default Index;