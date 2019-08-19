! ============================================
subroutine b4step2(mbc,mx,my,meqn,q,xlower,ylower,dx,dy,t,dt,maux,aux)
! ============================================
!
! # called before each call to step
! # use to set time-dependent aux arrays or perform other tasks.
!
! This particular routine sets negative values of q(1,i,j) to zero,
! as well as the corresponding q(m,i,j) for m=1,meqn.
! This is for problems where q(1,i,j) is a depth.
! This should occur only because of rounding error.
!
! Also calls movetopo if topography might be moving.

    use geoclaw_module, only: dry_tolerance
    use geoclaw_module, only: g => grav
    use topo_module, only: num_dtopo,topotime
    use topo_module, only: aux_finalized
    use topo_module, only: xlowdtopo,xhidtopo,ylowdtopo,yhidtopo

    use amr_module, only: xlowdomain => xlower
    use amr_module, only: ylowdomain => ylower
    use amr_module, only: xhidomain => xupper
    use amr_module, only: yhidomain => yupper
    use amr_module, only: xperdom,yperdom,spheredom,NEEDS_TO_BE_SET

    use storm_module, only: set_storm_fields
    implicit none

    ! Subroutine arguments
    integer, intent(in) :: meqn
    integer, intent(inout) :: mbc,mx,my,maux
    real(kind=8), intent(inout) :: xlower, ylower, dx, dy, t, dt
    real(kind=8), intent(inout) :: q(meqn,1-mbc:mx+mbc,1-mbc:my+mbc)
    real(kind=8), intent(inout) :: aux(maux,1-mbc:mx+mbc,1-mbc:my+mbc)


    ! Local storage
    integer :: index,i,j,k,dummy
    real(kind=8) :: h,u,v

    ! Check for NaNs in the solution
    call check4nans(meqn,mbc,mx,my,q,t,1)

    ! check for h < 0 and reset to zero
    ! check for h < drytolerance
    ! set hu = hv = 0 in all these cells
    forall(i=1-mbc:mx+mbc, j=1-mbc:my+mbc,q(1,i,j) < dry_tolerance)
        q(1,i,j) = max(q(1,i,j),0.d0)
        q(2:3,i,j) = 0.d0
    end forall


    if (aux_finalized < 2) then
        print *, 'RESETTING AUX'
        ! topo arrays might have been updated by dtopo more recently than
        ! aux arrays were set unless at least 1 step taken on all levels
        aux(1,:,:) = NEEDS_TO_BE_SET ! new system checks this val before setting
        call setaux(mbc,mx,my,xlower,ylower,dx,dy,maux,aux)
    endif

    ! !!!!!Change xlower and ylower compare values to varialbes read from file

   if ((xlower > -88.0) .and. (xlower < -86.0) .and. &
        (ylower < 26.0) .and. (ylower > 25.0)) then

           print *, 'Gonna call barrier breach!'
           call barrier_breach(maux,mbc,mx,my,xlower,ylower,dx,dy,t,dt,aux)

   end if

    ! Set wind and pressure aux variables for this grid
    call set_storm_fields(maux,mbc,mx,my,xlower,ylower,dx,dy,t,aux)

end subroutine b4step2

subroutine barrier_breach(maux,mbc,mx,my,xlower,ylower,dx,dy,t,dt,aux)
implicit none

! Allocate variables
! Subroutine variables
integer, intent(inout) :: mbc,mx,my,maux
real(kind=8), intent(inout) :: xlower, ylower, dx, dy, t, dt
real(kind=8), intent(inout) :: aux(maux,1-mbc:mx+mbc,1-mbc:my+mbc)

! Local variables
real(kind=8), allocatable, dimension(:) :: x, y, b
real(kind=8) :: db,depth
real,allocatable, dimension(:,:) :: X_mesh, Y_mesh, B_mesh, breach, bathy

CHARACTER(*), PARAMETER :: fileplace = "/home/claw/clawpack-v5.5.0/geoclaw/scratch/"

depth = minval(aux(1,i,j))
db = abs(depth / my-1)

call test_aux1(x, y, b, X_mesh, Y_mesh, B_mesh, bathy, depth, dx, dy, db, mx, my)

! fill x and y matrices a la np.meshgrid
allocate(X_mesh(size(y), size(x)))
allocate(Y_mesh(size(y), size(x)))
do i=1, size(y)
    do j=1, size(x)
        X_mesh(i,j) = x(j)
        Y_mesh(i,j) = y(i)
    end do
end do
! Add breach parameters
!!!!!! change these to imported from b4step2 subroutine
x2 = -86.0
x1 = -88.0
y1 = 25.5
y2 = 25.7
sigma = 10.0
h0 = 10.0
allocate(breach(size(X_mesh, 1), size(X_mesh, 2)))
! Initialize breach to match initial height
!do i= 1, size(X_mesh,2)
!	breach(:,i) = h0
!	do j = 1, size(X_mesh,1)
!		breach(j,:) = h0
!	end do
!end do
breach(:,:) = 0 ! aux(1, :, :)
! Breach the barrier island depending on time
if (t<t1) then
    amp =0.0
elseif (t>t1) then
    amp=10.0
end if

!!do i = 1, size(amp)
!open(99, file=fileplace//'breach_output.txt',status='new')
	do rowidx = 1, size(X_mesh, 1)
		row = X_mesh(rowidx,:)
			do colidx = 1, size(X_mesh, 2)
				col = X_mesh(rowidx, colidx)
        ycol = Y_mesh(rowidx, colidx)
        !print *, col, ycol
				if ((col >= x1) .and. (col <= x2) .and. &
           ( ycol >= y1) .and. (ycol <= y2)) then

					breach(rowidx, colidx) = breach(rowidx, colidx) &
					- (500.0 * exp(-col**2/(sigma**2))) ! exp(-X_mesh(rowidx, colidx)**2/(sigma**2)))
        !  print *, col,ycol, breach(rowidx, colidx)
          ! print *, breach(rowidx, colidx), aux(1,rowidx, colidx)
				end if
!        write(99) (breach(rowidx, colidx))
			end do
	end do
!close(99)
!end do


end subroutine barrier_breach
subroutine test_aux1(x, y, b, X_mesh, Y_mesh, B_mesh, bathy, depth, dx, dy, db, mx, my)
    real(kind=8), allocatable, dimension(:), intent(inout) :: x, y, b
    real(kind=8), allocatable, dimension(:,:), intent(inout) :: X_mesh, Y_mesh, B_mesh, bathy, depth
    real(kind=8), intent(inout) :: dx, dy, db
    

end subroutine test_aux1