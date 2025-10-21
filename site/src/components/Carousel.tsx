import { useState, useEffect, useCallback } from 'react';
import CampusDarcy from "assets/images/fotos/CampusDarcy.jpg";
import LAPPIS from "assets/images/fotos/lappis.png";
import Mamutes from "assets/images/fotos/MamutesDoCerrado.jpg";
import Orq from "assets/images/fotos/Orqstra.jpg";

const Carousel = () => {
  const [currentSlide, setCurrentSlide] = useState(0);

  const slides = [
    {
      id: 1,
      image: LAPPIS,
    },
    {
      id: 2,
      image: Orq,
    },
    {
      id: 3,
      image: Mamutes,
    },
    {
      id: 4,
      image: CampusDarcy,
    }
  ];

  const nextSlide = useCallback(() => {
    setCurrentSlide((prev) => (prev + 1) % slides.length);
  }, [slides.length]);

  useEffect(() => {
    const interval = setInterval(nextSlide, 5000);
    return () => clearInterval(interval);
  }, [nextSlide]);

  return (
    <div className="relative w-full max-w-4xl mx-auto">
      {/* Container responsivo - removi largura fixa */}
      <div className="carousel w-full h-[400px] rounded-box shadow-xl mx-auto">
        {slides.map((slide, index) => (
          <div
            key={slide.id}
            className={`carousel-item relative w-full h-full ${
              index === currentSlide ? 'block' : 'hidden'
            }`}
          >
            <img 
              src={slide.image} 
              className="w-full h-full object-cover"
              alt={`Slide ${index + 1}`}
            />
          </div>
        ))}
      </div>

      {/* Indicadores - centralizados corretamente */}
      <div className="flex justify-center w-full py-4 gap-2">
        {slides.map((_, index) => (
          <button
            key={index}
            onClick={() => setCurrentSlide(index)}
            className={`btn btn-xs ${index === currentSlide ? 'btn-primary' : 'btn-ghost'}`}
          >
            {index + 1}
          </button>
        ))}
      </div>
    </div>
  );
};

export default Carousel;