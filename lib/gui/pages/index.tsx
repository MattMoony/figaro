export default function Index() {
  return (
    <>
      <header>
        <h1>Figaro</h1>
        <div>
          Login
        </div>
      </header>
      <article>

      </article>
      <style jsx global>{`
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Open+Sans&display=swap');

        html, body {
          margin: 0;
          padding: 0;
          background-color: #0B3954;
        }
        
        header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 15px;
          background-color: #072435;
        }

        header h1 {
          font-weight: normal;
          font-family: 'Playfair Display', serif;
          margin: 0;
          color: #EEF1FF;
        }

        header div {
          background-color: #D14081;
          color: #EEF1FF;
          font-family: 'Open Sans', sans-serif;
          font-size: 1.1em;
          padding: 5px 10px;
          border-radius: 5px;
          transition: .2s ease;
        }

        header div:hover {
          cursor: pointer;
          transform: scale(1.1) rotate(2.5deg);
        }
      `}</style>
    </>
  );
};