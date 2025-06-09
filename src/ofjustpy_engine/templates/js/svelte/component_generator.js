function    createApp() {
    jpComponentBuilder.justpyComponents.set(justpyComponents);
    console.log("justpyComponents");
    console.log(justpyComponents)
    const allcomps = jpComponentBuilder.mount(jpComponentBuilder.App , {
	target: document.getElementById("components"),
      })
     // const allcomps = new jpComponentBuilder.App({
     // 	 target: document.getElementById("components"),
     // props: {
     //   name: "world",
     //   atag: "span",
     //   //justpyComponents : justpyComponents
     // },
     // });

    

// Old man hollow,pace to follow,peoples tree.half ten, half again century.rising sun, whence its done, cant you see?between hands,bellow them stands,yous it be  [this a code]                                                                                                    ANSWER-
  
  return allcomps;
  

}
